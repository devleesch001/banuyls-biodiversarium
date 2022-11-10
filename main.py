from flask import Flask, request
from parsers.ImerirParser import ImerirParser
import requests
import database_connector
import database_connector_factory

factory = database_connector_factory.SQLiteConnectorFactory("database")

def OK(result="done"):
    return ({"data":result}, 200)

def KO(err="unknown error"):
    return ({"error":err}, 500)

def BadRequest(reason="unknown error"):    
    return ({"error":reason}, 400)

def initdb():
    sql = factory.createConnection()
    print(sql.exists("Species"))
    if not sql.exists("Species"):
        sql.createTable("Species", {
            "fields":{
                "name":"varchar(50)",
                "familly":"varchar(50)",
                "common_name":"varchar(50)",
                "type":"varchar(20)",
                "description":"varchar(500)"
            },
            "primary":["name"]
        })
        sql.insert("Species", {
            "name":"example fish",
            "familly":"example",
            "common_name":"an example",
            "type":"example",
            "description":"this is actually a fish example"
        })
    sql.disconnect()

class CustomApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        print("server initialized")
        with self.app_context():
            initdb()
        super(CustomApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app=CustomApp(__name__)

@app.route("/fish", methods=["PATCH"])
def addOrUpdateFish():
    sql = factory.createConnection()
    if(sql.execute(sql.makeQuary()\
        .select("name").fromTable("Species")\
        .where(lambda w:w.init("name='"+request.form.get("name")+"'")), 1)[0] is not None):
        data = dict(request.form)
        data.pop("name", None)
        sql.update("Species",data)
    else:
        sql.insert("Species", request.form)
    sql.disconnect()
    return OK()

@app.route("/fish/<name>", methods=["DELETE"])
def deleteFish(name):
    sql = factory.createConnection()
    result = KO("Fish "+name+" not found")
    if sql.execute(sql.makeQuary()\
        .select("name").fromTable("Species")\
        .where(lambda w:w.init("name='"+name+"'")), 1)[0] is not None:
        sql.delete("Species", lambda w:w.init("name='"+name+"'"))
        result = OK("Fish deleted")
    sql.disconnect()
    return result

@app.route("/fish/<name>")
def getFish(name):
    sql = factory.createConnection()
    result = sql.execute(sql.makeQuary()\
        .select("*").fromTable("Species")
        .where(lambda w:w.init("name='"+name+"'")), 1)[0]
    sql.disconnect()
    if result is None:
        return KO("fish "+name+" not found")
    return OK(result)


@app.route("/fish")
def getAllFish():
    sql = factory.createConnection()
    result = [result for result in sql.execute(sql.makeQuary()\
        .select("*").fromTable("Species"))]
    sql.disconnect()
    return OK(result)

@app.route("/analyze/<ai_name>", methods=["POST"])
def analize(ai_name):
    image = request.form.get("image")
    imerirParser = ImerirParser()
    durl = ("adefaulturl[image]", imerirParser)
    urlparsermap = {
        "IMERIR":("theimerirurl[image]", imerirParser),
        "GOOGLE":("googlelensurl[image]", imerirParser)
    }
    rurl, parser = urlparsermap[ai_name.upper()] if ai_name in urlparsermap else durl
    return OK(parser.parse(requests.get(rurl.replace("[image]", image))))

if __name__ == "__main__":
    app.run()