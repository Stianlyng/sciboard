import os
#from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """
        Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
        """

    DEBUG = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') # Viktig for logging til Heroku
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = 'A terrible secret key' or 'badabim badabom'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'databases/app.db')

class TestingConfig(Config):
    TESTING = False
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True # Hva betyr dette?
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'databases/test.db')

class ProductionConfig(Config):

    # Google Cloud Database Server
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://stian:Vanilje2710@35.228.21.4:3306/openresearch'

    # Kark UIT Database Server
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://stud_v22_straetesti:deny impeach dreadlock fondly@kark.uit.no:3306/stud_v22_straetesti"

