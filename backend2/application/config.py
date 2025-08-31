class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://127.0.0.1:6379/0'  
    CACHE_DEFAULT_TIMEOUT = 10  

class LoadDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///parkingdb.sqlite3"
    JWT_SECRET_KEY = "this is a secret key"   
     