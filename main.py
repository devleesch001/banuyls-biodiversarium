from flask import Flask, request
from parsers.ImerirParser import ImerirParser
import requests
import database_connector
import database_connector_factory
import io
import re
import base64
import binascii
import imghdr
import vision_controller

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
    result = BadRequest("Fish "+name+" not found")
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
        return BadRequest("fish "+name+" not found")
    return OK(result)


@app.route("/fish")
def getAllFish():
    sql = factory.createConnection()
    result = [result for result in sql.execute(sql.makeQuary()\
        .select("*").fromTable("Species"))]
    sql.disconnect()
    return OK(result)

@app.route("/analyze/<ai_name>", methods=["POST"])
def analyze(ai_name):
    request_data = request.json

    if 'content' not in request_data:
        return BadRequest('No field content')

    # Removes base64 header
    img_content = re.sub("data:image\/.*;base64,", "", request_data['content'])
    try:
        contentDecode = base64.b64decode(img_content, validate=False)
    except binascii.Error:
        return BadRequest('Field content is in an invalid base64 format')

    # Checks if the content is an image
    if imghdr.what(None, contentDecode) == None:
        return BadRequest('Field content is not an image')

    results = vision_controller.get_labels(contentDecode)

    return OK(results)

if __name__ == "__main__":
    app.run()
