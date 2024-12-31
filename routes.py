from flask import render_template, request, abort, flash, redirect, url_for
import os, uuid
from models import Image
from io import BytesIO
from app import db
import base64

def init_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def upload_image():
        image_preview = None
        link = None

        if request.method == 'POST':
            image = request.files['image']
            if image:
                try:
                    # Save the image to the upload folder
                    filename = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + '.' + image.filename.split('.')[-1])
                    image.save(filename)
                    print(f"Saved image to {filename}")

                    # Encrypt and save the image
                    with open(filename, 'rb') as file:
                        file_data = app.fernet.encrypt(file.read())

                    image_name = str(uuid.uuid4())
                    new_image = Image(id=image_name, data=file_data)
                    db.session.add(new_image)
                    db.session.commit()

                    # Remove the saved file after it's encrypted and stored in the database
                    os.remove(filename)

                    # Generate image preview
                    img_byte_array = BytesIO(app.fernet.decrypt(new_image.data))
                    img_byte_array.seek(0)
                    img_preview = base64.b64encode(img_byte_array.read()).decode('utf-8')

                    # Generate the shareable link
                    link = f"{request.url_root}view/{image_name}"

                    # Return the page with image preview and link
                    return render_template('upload.html', image_preview=f"data:image/png;base64,{img_preview}", link=link)
                except Exception as e:
                    db.session.rollback()  # Rollback in case of any error
                    flash(f"An error occurred while uploading the image: {str(e)}")
                    return redirect(url_for('upload_image'))

        return render_template('upload.html', image_preview=image_preview, link=link)

    @app.route('/view/<image_id>')
    def view_image(image_id):
        image = Image.query.get(image_id)
        if not image:
            abort(404)

        try:
            # Decrypt image
            decrypted_data = app.fernet.decrypt(image.data)
            db.session.delete(image)  # Delete the image after one-time view
            db.session.commit()

            # Convert image bytes to base64
            img_base64 = base64.b64encode(decrypted_data).decode('utf-8')

            return render_template('view.html', image_data=img_base64)
        except Exception as e:
            flash(f"Error occurred while decrypting the image: {str(e)}")
            return redirect(url_for('upload_image'))
