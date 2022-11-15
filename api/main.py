from builtins import str

from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, Text, update, delete, select
import json
import argparse
from sqlalchemy.sql import func
from flask_cors import CORS
import re
import base64
import binascii
import imghdr
# import vision_controller
import imerir_controller

app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aquarium.db"

db = SQLAlchemy(app)
db.init_app(app)

MOBILE_AI = "IMERIR"


def OK(result="Done"):
    return ({"data": result}, 200)


def KO(err="UNKNW"):
    return ({"error": err}, 500)


def BadRequest(reason="UNKNW"):
    return ({"error": reason}, 400)


CORS(app)


def checks(request_data):
    if 'content' not in request_data:
        return (False, BadRequest('NOCONTENT'))

    # Removes base64 header
    img_content = re.sub("data:image\/.*;base64,", "", request_data['content'])
    try:
        contentDecode = base64.b64decode(img_content, validate=False)
    except binascii.Error:
        return (False, BadRequest('CONTENTBADFORMAT'))

    # Checks if the content is an image
    if imghdr.what(None, contentDecode) == None:
        return (False, BadRequest('CONTENTNOIMAGE'))

    return (True, contentDecode)


@app.route("/api/mobile/analyze", methods=["POST"])
def analyzeMobile():
    check = checks(request.json)
    if check[0]:
        contentDecode = check[1]
        if MOBILE_AI == "IMERIR":
            results = imerir_controller.get_labels(contentDecode)
        """else:
            results = vision_controller.get_labels(contentDecode)"""
    else:
        return check[1]
    return OK(results)


@app.route("/api/tablet/analyze", methods=["POST"])
def analyzeTablet():
    check = checks(request.json)
    if check[0]:
        contentDecode = check[1]
        results = imerir_controller.get_labels(contentDecode)
    else:
        return check[1]
    return OK(results)


class Species(db.Model):
    id = db.Column(Integer, primary_key=True)
    scientific_name = db.Column(String(50))
    name = db.Column(String(50))
    family = db.Column(String(50))
    description = db.Column(Text)
    s_type = db.Column(String(20))

    def __init__(self, scientific_name: str, name: str, family: str, description: str, s_type: str):
        self.scientific_name = scientific_name
        self.name = name
        self.family = family
        self.description = description
        self.s_type = s_type

    def toDict(self):
        return {"scientific_name": self.scientific_name, "name": self.name, "family": self.family,
                "description": json.loads(self.description), "type": self.s_type}

    def __repr__(self):
        return f'<Species {self.scientific_name}>'

    def json(self):
        return {
            "id":self.id,
            "s_name":self.scientific_name,
            "name":self.name,
            "family":self.family,
            "description":self.description,
            "type":self.s_type
        }


with app.app_context():
    db.create_all()

def toList(scalar):
    list = []
    for item in scalar:
        list.append(item.json())
    return list


@app.route('/api', methods=["GET"])
def hello_world():  # put application's code here
    return OK("hello world!")


@app.route("/api/species", methods=["GET"])
def species_list():
    species = Species.query.all()
    species_serialized = [element.toDict() for element in species]

    return OK(species_serialized)

@app.route("/api/species/<s_name>")
def speccy(s_name):
    species = db.session.execute(
        db.select(Species).where(Species.scientific_name == s_name)).scalars()
    return OK(toList(species))


@app.route("/api/species/<tmp_name>")
def autocmpl(tmp_name):
    
    # result = db.session.query(Species.name).filter(Species.name.like('%'+tmp_name+'%'))
    # return OK(toList(result))

    species = db.session.execute(
        db.select(Species.name).where(tmp_name in Species.name)).scalars()
    return OK(toList(species))


@app.route("/api/species_create", methods=["POST"])
def species_create():
    
    speccy = Species(
        scientific_name=request.json["s_name"],
        name=request.json["name"],
        family=request.json["family"],
        s_type=request.json["type"],
        description=request.json["description"]
    )
    db.session.add(speccy)
    db.session.commit()
    return OK()

@app.route("/api/species_delete/<id>", methods=["DELETE"])
def species_delete(id):
    if(len(toList(db.session.execute(
        db.select(Species).where(Species.id == id)).scalars())) == 0):
        return BadRequest("FISHNOFOUND")
    db.session.execute(        
        delete(Species).where(Species.id == id)  
    )
    db.session.commit()
    return OK()


@app.route("/api/update_speccy", methods=["POST"])
def update_species():  
    if(len(db.session.execute(
        db.select(Species).where(Species.id == request.form["id"])).scalars()) == 0):
        return BadRequest("FISHNOFOUND")
    speccy = Species(
        scientific_name=request.form["s_name"],
        name=request.form["name"],
        family=request.form["family"],
        s_type=request.form["s_type"],
        description=request.form["description"]
    )        
    db.session.execute(
        update(Species).values(speccy).where(Species.id == request.form["id"])   
    )
    db.session.commit()
    return OK()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API")
    parser.add_argument("-p", "--port", default=5000, type=int, help="port number")
    parser.add_argument("-d", "--debug", default=False, type=bool, help="Debug")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port, debug=args.debug)
