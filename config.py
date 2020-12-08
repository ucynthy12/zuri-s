import os
class Config:
    '''
    Generl configuration parent class
    '''
     
    BLOG_BASE_URL= 'http://quotes.stormconsultancy.co.uk/random.json'

    SECRET_KEY= os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://cynt:zion@localhost/zuri'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
#  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class ProdConfig(Config):
    pass

class DevConfig(Config) :
    BLOG_BASE_URL= 'http://quotes.stormconsultancy.co.uk/random.json'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://cynt:zion@localhost/zuri'
    DEBUG = True

config_options = {
    'development' : DevConfig,
    'production' :ProdConfig
}

