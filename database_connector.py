import abc
import sqlite3
from sqlite3 import Error
from typing import Callable, Dict, List

class DatabaseConnector(abc.ABC):
    @abc.abstractclassmethod
    def connect(self, host, user, password):
        pass

    @abc.abstractclassmethod
    def send(self, query):
        pass

    @abc.abstractclassmethod
    def createTable(self, table_name, table_spec):
        pass

    @abc.abstractclassmethod
    def insert(self, table_name, values):
        pass

    @abc.abstractclassmethod
    def update(self, table_name, values, selector=None):
        pass

    @abc.abstractclassmethod
    def delete(self, table_name, id):
        pass

    @abc.abstractclassmethod
    def exists(self, table_name):
        pass

class QueryMaker(abc.ABC):
    class TableSelector():
        def __init__(self):
            self.tables = []

        def join(self, table, joinspecs, join="natural"):
            fromt = None
            tot = None
            if "using" in joinspecs:
                fromt = tot = joinspecs["using"]
            else:
                fromt = joinspecs["from"]
                tot = joinspecs["to"]
            self.tables.append((join, table, fromt, tot))
            return self

    class WhereMaker():
        def __init__(self):
            self.clause = ""

        def init(self, clause):
            if self.clause != "":
                return self
            self.clause = clause
            return self

        def andClause(self, clause):
            if self.clause == "":
                return self.init(clause)
            self.clause+=" AND "+clause
            return self

        def orClause(self, clause):
            if self.clause == "":
                return self.init(clause)
            self.clause+=" OR "+clause
            return self

    def __init__(self):
        self.whereclause=None
        self.selected = []
        self.tables=[]
    
    def select(self, selections):
        self.selected.extend(selections if type(selections) == List[str] else [selections])
        return self
    
    def fromTable(self, table, joins = None):
        self.tables = [(None, table, None, None)]
        if type(joins) == type(lambda:None):
            selector = QueryMaker.TableSelector()
            joins(selector)
            self.tables.extend(selector.tables)
        elif type(joins) == type({"":{"":""}}):
            for jtable, join in joins.items():                
                fromt = None
                tot = None
                if "using" in join:
                    fromt = tot = join["using"]
                else:
                    fromt = join["from"]
                    tot=join["to"]
                self.tables.append((join["type"] if "type" in join else "netural"
                , jtable, fromt, tot))
        elif(joins is not None):
            print("WARN: joins argument must be a callable of type (QueryMaker.TableSelector)=>None or a dict, ignoring join clauses")
        return self
        
    def where(self, where):
        maker = QueryMaker.WhereMaker()
        where(maker)
        self.whereclause=maker.clause
        return self
    
    @abc.abstractclassmethod
    def build(self):
        pass

class SqlDatabaseConnector(DatabaseConnector):

    class SqliteQueryMaker(QueryMaker):     
        
        def build(self, formated=False):
            query = "SELECT"
            for select in self.selected:
                query += " "+select
            if formated:
                query += "\n"
            query += "FROM "
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

    def createTable(self, table_name, table_spec):
        query = "CREATE TABLE "+table_name+"("
        query += ",".join(field+" "+type for field, type in table_spec["fields"].items())
        if "primary" in table_spec:
            query += ","+",".join("PRIMARY KEY("+primary+")" for primary in table_spec["primary"])
        if "foreign" in table_spec:
            query += ","+",".join(["FOREIGN KEY("+foreign+") REFERENCES "+table_spec["forein"][foreign]["table"]+"("+table_spec["forein"][foreign]["field"]+")" for foreign in table_spec["forein"]])
        query+=");"
        return self.send(query)

    def insert(self, table_name, values):
        query = "INSERT INTO "+table_name+"("        
        query+=",".join(values.keys())
        query += ") VALUES("
        query+=",".join(["'"+str(x)+"'" for x in values.values()])
        query += ");"
        return self.send(query)

    def update(self, table_name, values, selector=None):        
        query = "UPDATE TABLE "+table_name      
        query+=" SET "+",".join([field+"='"+str(value)+"'" for field, value in values.items()])
        if selector is not None:
            maker = QueryMaker.WhereMaker()
            selector(maker)
            query+=" WHERE "+maker.clause
        query += ";"
        return self.send(query)

    def delete(self, table_name, where):
        query = "DELETE FROM "+table_name        
        maker = QueryMaker.WhereMaker()
        where(maker)
        query+=" WHERE "+maker.clause+";"
        return self.send(query)

class SqliteDatabaseConnector(SqlDatabaseConnector):
    def __init__(self):
        DatabaseConnector.__init__(self)
        self.conn = None
    
    def connect(self, host, user="", password=""):
        try:
            self.conn = sqlite3.connect(host)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def exists(self, table_name):
        return len(self.send("SELECT name FROM sqlite_master WHERE type='table' AND name='"+table_name+"';"))>0

    def send(self, query):
        print(query)
        c = self.conn.cursor()
        c.execute(query)
        return c.fetchall()