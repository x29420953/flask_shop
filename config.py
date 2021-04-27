class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://b1ad405ad73ea5:25c66eb7@us-cdbr-east-03.cleardb.com/heroku_637d5fce379a2f7"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = "My Key"
    SECRET_KEY = "Your Key"
    #mysql://b1ad405ad73ea5:25c66eb7@us-cdbr-east-03.cleardb.com/heroku_637d5fce379a2f7?reconnect=true
    #mysql+pymysql://root:88888888@127.0.0.1:3307/shop