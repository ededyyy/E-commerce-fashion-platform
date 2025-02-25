import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'a-very-secret-secret'

# email config
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_TLS = True
MAIL_PORT = 587
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '965061749@qq.com')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'jdrfgotxeqikbcja')
MAIL_DEFAULT_SENDER = "965061749@qq.com"


# upload img config
UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'img')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
