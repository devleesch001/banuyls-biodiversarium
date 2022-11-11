from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, Text
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


def OK(result="done"):
    return ({"data": result}, 200)


def KO(err="unknown error"):
    return ({"error": err}, 500)


def BadRequest(reason="unknown error"):
    return ({"error": reason}, 400)


CORS(app)


def checks(request_data):
    if 'content' not in request_data:
        return (False, BadRequest('No field content'))

    # Removes base64 header
    img_content = re.sub("data:image\/.*;base64,", "", request_data['content'])
    try:
        contentDecode = base64.b64decode(img_content, validate=False)
    except binascii.Error:
        return (False, BadRequest('Field content is in an invalid base64 format'))

    # Checks if the content is an image
    if imghdr.what(None, contentDecode) == None:
        return (False, BadRequest('Field content is not an image'))

    return (True, contentDecode)


@app.route("/mobile/analyze", methods=["POST"])
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


@app.route("/tablet/analyze", methods=["POST"])
def analyzeTablet():
    check = checks(request.json)
    if check[0]:
        contentDecode = check[1]
        results = imerir_controller.get_labels(contentDecode)
    else:
        return check[1]
    return OK(results)


class Species(db.Model):
    id = Column(Integer, primary_key=True)
    scientific_name = Column(String(50))
    name = Column(String(50))
    family = Column(String(50))
    description = Column(Text)
    s_type = Column(String(20))

    def __repr__(self):
        return f'<Species {self.s_name}>'


with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return {'message': "Hello World!'"}


@app.route("/species")
def species_list():
    species = db.session.execute(
        db.select(Species).order_by(Species.scientific_name)).scalars()
    for specy in species:
        print("Species: " + specy.name)
    return render_template("species_list.html", species=species)


@app.route("/species_create", methods=["GET", "POST"])
def species_create():
    if request.method == "POST":
        speccy = Species(
            scientific_name=request.form["s_name"],
            name=request.form["name"],
            family=request.form["family"],
            s_type=request.form["s_type"],
            description=json.dumps({"fr": request.form["description"]})
        )
        db.session.add(speccy)
        db.session.commit()
        return redirect(url_for("species_list", scientific_name=speccy.scientific_name))

    return render_template("create_species.html")


@app.route("/update_species", methods=["GET", "POST"])
def update_species():
    return render_template("species_list.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API")
    parser.add_argument("-p", "--port", default=5000, type=int, help="port number")
    parser.add_argument("-d", "--debug", default=False, type=bool, help="Debug")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port, debug=args.debug)
