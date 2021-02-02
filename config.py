from database.inmemory import UserStruct


class ConfigMySQL:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:test@localhost/users'
    SQLALCHEMY_ECHO = False
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigSQLite:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.users'
    SQLALCHEMY_ECHO = False
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigInMemoryDataBase():
    def __init__(self, db=UserStruct()):
        self.db = db