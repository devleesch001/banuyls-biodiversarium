from flask import Flask
from parsers.ImerirParser import ImerirParser
import requests
import database_connector

app=Flask(__name__)

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

builder = database_connector.SqliteDatabaseConnector.SqliteQueryMaker()\
    .select("example")\
    .fromTable("table", lambda joins:joins
        .join("another", {"using":"id"})
        .join("yetanother", {"from":"id", "to":"anotherid"}))\
    .where(lambda where:where.init("example.id=0").andClause("another.afield='value'"))

database_connector.SqliteDatabaseConnector().createTable(
    "table",
    {
        "fields":{
            "id":"int(10)",
            "field":"varchar(5)",
        },
        "primary":["id"]
    }
)

database_connector.SqliteDatabaseConnector().insert(
    "table",
    {
        "id":0,
        "field":"value"
    }
)

database_connector.SqliteDatabaseConnector().update(
    "table",
    {
        "id":0,
        "field":"value"
    },
    lambda cond:cond.init("id=0")
)

database_connector.SqliteDatabaseConnector().delete(
    "table",
    lambda cond:cond.init("id=0")
)

print(builder.build(formated=True))
    
