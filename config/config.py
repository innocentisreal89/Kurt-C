import os
import re
from decouple import config  # we'll use config package in this decouple to read the secret key in the .env file
from datetime import timedelta

#   the path to our datatbase
base_dir = os.path.dirname(os.path.realpath(__file__))

# uri =config('DATABASE_URL')
# if uri.startswith('posgres://'):
#     uri = uri.replace('postgres://', 'postgresql://', 1)
    
class Config:
    SECRET_KEY = config('SECRET_KEY')

class DevConfig(Config):
    DEBUG = config('DEBUG', True, cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite3')

class TestConfig(Config):
    # TESTING = True
    # SQLALCHEMY_ECHO = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite://' 
    pass

class ProdConfig(Config):
    # SQLALCHEMY_DATABASE_URI = uri               
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DEBUG = config('DEBUG', False, cast=bool)
    pass
    
   


#this config_dict is created so dat we can easily read/hold these classes
config_dict = {
    'dev':DevConfig,
    'test':TestConfig,
    'prod':ProdConfig
}