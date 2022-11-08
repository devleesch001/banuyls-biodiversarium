from flask import Flask
from parsers.ImerirParser import ImerirParser
import requests
import database_connector

app=Flask(__name__)
sql = database_connector.SqliteDatabaseConnector()
sql.connect("database")
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

@app.route("/")
def root():
    return "<p>root</p>"

@app.route("/analize/{ai_name}/{image}")
def analize(ai_name, image):
    imerirParser = ImerirParser()
    durl = ("adefaulturl[image]", imerirParser)
    urlparsermap = {
        "IMERIR":("theimerirurl[image]", imerirParser),
        "GOOGLE":("googlelensurl[image]", imerirParser)
    }
    rurl, parser = urlparsermap[ai_name.upper()] if ai_name in urlparsermap else durl
    return parser.parse(requests.get(rurl.replace("[image]", image)))
    
