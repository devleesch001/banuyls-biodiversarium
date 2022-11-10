import abc
from typing import List

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
        self.fromTableName = ""
    
    def select(self, selections):
        self.selected.extend(selections if type(selections) == List[str] else [selections])
        return self
    
    def fromTable(self, table, joins = None):
        self.tables = [(None, table, None, None)]
        self.fromTableName = table
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
