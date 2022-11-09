from flask import Flask, request
import os
from parsers.ImerirParser import ImerirParser
import requests
import database_connector

import io
import re
import base64
import binascii
import imghdr
import vision_controller

def getSqlConnection():
    sql = database_connector.SqliteDatabaseConnector()
    sql.connect("database")
    return sql

def OK(result):
    return (result, 200)

def KO(err):
    return (err, 400)

def initdb():
    sql = getSqlConnection()
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

@app.route("/")
def root():
    return "<p>root</p>"

@app.route("/pushfish", methods=["PUSH"])
def addOrUpdateFish():
    sql = getSqlConnection()
    result = None
    if(sql.execute(sql.makeQuary()\
        .select("name").fromTable("Species")\
        .where(lambda w:w.init("name='"+request.form.get("name")+"'"))), 1):
        result = sql.update("Species", request.form)
    else:
        result = sql.insert("Species", request.form)
    sql.disconnect()
    return OK(result)

@app.route("/deletefish/<name>", methods=["DELETE"])
def deleteFish(name):
    sql = getSqlConnection()
    result = KO("Fish "+name+" not found")
    if(sql.execute(sql.makeQuary()\
        .select("name").fromTable("Species")\
        .where(lambda w:w.init("name='"+name+"'"))), 1):
        sql.delete("Species", lambda w:w.init("name='"+name+"'"))
        result = OK("Fish deleted")
    sql.disconnect()
    return result

@app.route("/fish/<name>")
def getFish(name):
    sql = getSqlConnection()
    result = sql.execute(sql.makeQuary()\
        .select("*").fromTable("Species")
        .where(lambda w:w.init("name='"+name+"'")), 1)
    sql.disconnect()
    return OK({
        "name":result[0],
        "familly":result[1],
        "common_name":result[2],
        "type":result[3],
        "description":result[4]
    })


@app.route("/fish")
def getAllFish():
    sql = getSqlConnection()
    result = [{
        "name":result[0],
        "familly":result[1],
        "common_name":result[2],
        "type":result[3],
        "description":result[4]
    } for result in sql.execute(sql.makeQuary()\
        .select("*").fromTable("Species"))]
    sql.disconnect()
    return OK(result)

@app.route("/analyze/<ai_name>", methods=["POST"])
def analyze(ai_name):
    request_data = request.json

    if 'content' not in request_data:
        return KO({'error': 'No field content'})

    # Removes base64 header
    img_content = re.sub("data:image\/.*;base64,", "", request_data['content'])
    try:
        contentDecode = base64.b64decode(img_content, validate=False)
    except binascii.Error:
        return KO({'error': 'Field content is in an invalid base64 format'})

    # Checks if the content is an image
    if imghdr.what(None, contentDecode) == None:
        return KO({'error': 'Field content is not an image'})

    results = vision_controller.get_labels(contentDecode)

    return OK(results)

    # image = request.form.get("image")
    # imerirParser = ImerirParser()
    # durl = ("adefaulturl[image]", imerirParser)
    # urlparsermap = {
    #     "IMERIR":("theimerirurl[image]", imerirParser),
    #     "GOOGLE":("googlelensurl[image]", imerirParser)
    # }
    # rurl, parser = urlparsermap[ai_name.upper()] if ai_name in urlparsermap else durl
    # return OK(parser.parse(requests.get(rurl.replace("[image]", image))))

if __name__ == "__main__":
    app.run()
