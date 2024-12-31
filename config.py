from cryptography.fernet import Fernet
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key generation: This should be kept secure in production!
SECRET_KEY = Fernet.generate_key()
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
