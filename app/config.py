from datetime import timedelta

class Config:
    USER_TABLE = 'user',
    JWT_SECRET_KEY='SLDKFJSDLKJFSJFK55454544R4##'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)