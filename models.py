from app import db

class Image(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
