import database_connector
import abc

class DatabaseConnectorFactory(abc.ABC):
    def __init__(self, host:str, user:str="", password:str=""):
        self.host = host
        self.user = user
        self.password=password

    @abc.abstractclassmethod
    def createConnection(self)->database_connector.DatabaseConnector:
        pass

class SQLiteConnectorFactory(DatabaseConnectorFactory):
    
    def createConnection(self)->database_connector.DatabaseConnector:
        database = database_connector.SqliteDatabaseConnector()
        database.connect(self.host, self.user, self.password)
        return database

    