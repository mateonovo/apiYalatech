from os import environ
import pyodbc
from sqlalchemy import create_engine
class Config(object):
    # Clase base

    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"



class DevelopmentConfig(Config):
 pass
    
    
class TestingConfig(Config):
    # Configuracion de testeo

    TESTING = True


config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
}
