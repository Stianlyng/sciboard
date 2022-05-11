import os
#from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, '.env'))


class Config:

    DEBUG = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') # Viktig for logging til Heroku
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = 'A terrible secret key' or 'badabim badabom'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'sciboard.org@gmail.com'
    MAIL_PASSWORD = 'Activate Commend7 Slip'
    ADMINS = ['sciboard.org@gmail.com']

class DevelopmentConfig(Config):

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'databases/app.db')

class TestingConfig(Config):
    TESTING = False
    WTF_CSRF_ENABLED = True
    MAIL_SUPPRESS_SEND = False # Hva betyr dette?
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'databases/test.db')

class ProductionConfig(Config):

    # Google Cloud Database Server
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://stian:Vanilje2710@35.228.21.4:3306/openresearch'

    # Kark UIT Database Server
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://stud_v22_straetesti:deny impeach dreadlock fondly@kark.uit.no:3306/stud_v22_straetesti"

