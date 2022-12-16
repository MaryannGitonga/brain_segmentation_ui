from os import environ, path
import os
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """"Set Flask Configuration from environment variables"""
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")
    
    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')
    
    # Flask-SQLAlchemy
    if FLASK_ENV == 'development':
        SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
        SQLALCHEMY_ECHO = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    elif FLASK_ENV == 'production':
        DEBUG = False
        ALLOWED_HOSTS = [environ.get('WEBSITE_HOSTNAME')] if 'WEBSITE_HOSTNAME' in os.environ else []
        CSRF_TRUSTED_ORIGINS = ['https://'+ environ.get('WEBSITE_HOSTNAME')] if 'WEBSITE_HOSTNAME' in os.environ else []
        
        # Configure Postgres database; the full username for PostgreSQL flexible server is
        # username (not @sever-name).
        DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=environ.get('DBUSER'),
            dbpass=environ.get('DBPASS'),
            dbhost=environ.get('DBHOST') + ".postgres.database.azure.com",
            dbname=environ.get('DBNAME')
        )
    
    # Flask-Assets
    LESS_BIN = environ.get("LESS_BIN")
    ASSETS_DEBUG = environ.get("ASSETS_DEBUG")
    LESS_RUN_IN_DEBUG = environ.get("LESS_RUN_IN_DEBUG")