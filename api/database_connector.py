import abc
import sqlite3
from query_maker import QueryMaker
from sqlite3 import Error
from typing import Dict, Callable, List, Tuple

UNUSED = lambda x:x

SQL_DATA_TYPE = float|int|str
SQL_VALUES_TYPE = Dict[str, SQL_DATA_TYPE]
TABLE_SPEC_TYPE = Dict[str, str|Dict[str, str]]
SELECTOR_TYPE = Callable[[QueryMaker], str]
SQL_RETURN_TYPE = List[Dict]

class DatabaseConnector(abc.ABC):

    def __init__(self):
        self.tableSpecs:Dict[str, List[str]] = {}

    @abc.abstractclassmethod
    def connect(self, host:str, user:str, password:str)->bool:
        pass

    @abc.abstractclassmethod
    def disconnect(self)->None:
        pass

    @abc.abstractclassmethod
    def send(self, parseValues:Dict[int, str], query:str)->SQL_RETURN_TYPE:
        pass

    @abc.abstractclassmethod
    def createTable(self, table_name:str, table_spec:TABLE_SPEC_TYPE)->SQL_RETURN_TYPE:
        pass

    @abc.abstractclassmethod
    def insert(self, table_name:str, values:SQL_VALUES_TYPE)->SQL_RETURN_TYPE:
        pass

    @abc.abstractclassmethod
    def update(self, table_name:str, values:SQL_VALUES_TYPE, selector:SELECTOR_TYPE=None)->SQL_RETURN_TYPE:
        pass

    @abc.abstractclassmethod
    def delete(self, table_name:str, where:SELECTOR_TYPE)->SQL_RETURN_TYPE:
        pass

    @abc.abstractclassmethod
    def exists(self, table_name:str)->bool:
        pass

    @abc.abstractclassmethod
    def makeQuary(self)->QueryMaker:
        pass

class SqlDatabaseConnector(DatabaseConnector):

    class SqlQueryMaker(QueryMaker):     
        
        def build(self, formated:bool=False)->str:
            query = "SELECT"
            for select in self.selected:
                query += " "+select
            if formated:
                query += "\n"
            query += " FROM"
            previousTable = None
            for i in range(len(self.tables)):
                join = self.tables[i]
                query += " "+((join[0].upper()+" join ") if join[0] is not None else "")+join[1]+((" on "+previousTable+"."+join[2]+"="+join[1]+"."+join[3]) if join[0] is not None else "")
                previousTable = join[1]
            if formated:
                query += "\n"
            if self.whereclause is not None:
                query+=" WHERE "+self.whereclause
            return query+";"

    def __init__(self):
        DatabaseConnector.__init__(self)

    def makeQuary(self)->QueryMaker:
        return SqlDatabaseConnector.SqlQueryMaker()

    def execute(self, maker:QueryMaker, limit:int = 0)->SQL_RETURN_TYPE:
        return self.send(maker.build(), parseValues=self.tableSpecs[maker.fromTableName], limit=limit)

    def createTable(self, table_name:str, table_spec:TABLE_SPEC_TYPE)->SQL_RETURN_TYPE:
        query = "CREATE TABLE "+table_name+"("
        query += ",".join(field+" "+type for field, type in table_spec["fields"].items())
        if "primary" in table_spec:
            query += ","+",".join("PRIMARY KEY("+primary+")" for primary in table_spec["primary"])
        if "foreign" in table_spec:
            query += ","+",".join(["FOREIGN KEY("+foreign+") REFERENCES "+table_spec["forein"][foreign]["table"]+"("+table_spec["forein"][foreign]["field"]+")" for foreign in table_spec["forein"]])
        query+=");"
        try:
            self.send(query)
            self.tableSpecs[table_name] = table_spec["fields"].keys()
            return {"result":"OK"}
        except Exception as e:
            return {"result":"KO", "reason":str(e)}

    def insert(self, table_name:str, values:SQL_VALUES_TYPE)->SQL_RETURN_TYPE:
        query = "INSERT INTO "+table_name+"("        
        query+=",".join(values.keys())
        query += ") VALUES("
        query+=",".join(["'"+str(x)+"'" for x in values.values()])
        query += ");"        
        try:
            self.send(query)
            return {"result":"OK"}
        except Exception as e:
            return {"result":"KO", "reason":str(e)}

    def update(self, table_name:str, values:SQL_VALUES_TYPE, selector:SELECTOR_TYPE=None)->SQL_RETURN_TYPE:        
        query = "UPDATE "+table_name      
        query+=" SET "+",".join([field+"='"+str(value)+"'" for field, value in values.items()])
        if selector is not None:
            maker = QueryMaker.WhereMaker()
            selector(maker)
            query+=" WHERE "+maker.clause
        query += ";"
        try:
            self.send(query)
            return {"result":"OK"}
        except Exception as e:
            return {"result":"KO", "reason":str(e)}

    def delete(self, table_name:str, where:SELECTOR_TYPE)->SQL_RETURN_TYPE:
        query = "DELETE FROM "+table_name        
        maker = QueryMaker.WhereMaker()
        where(maker)
        query+=" WHERE "+maker.clause+";"
        try:
            self.send(query)
            return {"result":"OK"}
        except Exception as e:
            return {"result":"KO", "reason":str(e)}

class SqliteDatabaseConnector(SqlDatabaseConnector):
    def __init__(self):
        SqlDatabaseConnector.__init__(self)
        self.conn = None
    
    def connect(self, host:str, user:str="", password:str="")->bool:
        UNUSED(user)
        UNUSED(password)
        try:
            self.conn = sqlite3.connect(host)
            tables = self.send("SELECT name FROM sqlite_master WHERE type='table'")
            for table in tables[0]:
                columns = self.send("PRAGMA table_info("+table+");")
                tableSpec = {}
                for column in columns:
                    tableSpec[column[0]] = column[1]
                self.tableSpecs[table]=tableSpec
            return True
        except Error as e:
            print(e)
            return False

    def exists(self, table_name:str)->bool:
        return len(self.send("SELECT name FROM sqlite_master WHERE type='table' AND name='"+table_name+"';"))>0

    def send(self, query:str, parseValues:Dict[int, str]=None, limit:int = 0)->SQL_RETURN_TYPE:
        if limit == 0:result = self.conn.execute(query).fetchall()
        elif limit == 1:result = [self.conn.execute(query).fetchone()]
        else:result = self.conn.execute(query).fetchmany(limit)
        self.conn.commit()
        parsed = []
        for value in result:
            if value is None:
                parsed.append(None)
            else:
                if parseValues is not None:
                    data = {}
                    for i in range(len(value)):
                        data[parseValues[i]]=value[i]
                    parsed.append(data)
                else:
                    parsed.append(value)
        return parsed

    def disconnect(self)->bool:
        try:
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False