

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:88888888@127.0.0.1:3307/shop"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = "My Key"
    SECRET_KEY = "Your Key"
    