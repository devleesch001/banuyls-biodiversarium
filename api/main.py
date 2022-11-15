from builtins import str

from flask import Flask, g, request, render_template, url_for, redirect
from flask_oauthlib.provider import OAuth2Provider
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, Text, BLOB, update, delete, select
import json
import argparse
from sqlalchemy.sql import func
from flask_cors import CORS
import re
import base64
import binascii
import imghdr
import imerir_controller
from oauth import init
from datetime import datetime, timedelta
from functools import wraps

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__, template_folder='templates')
oauth = OAuth2Provider(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aquarium.db"

db = SQLAlchemy(app)
db.init_app(app)

MOBILE_AI = "IMERIR"

Client, User, Grant, Token=init(db)

@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()

@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=User.query.filter_by(id=request.client.user_id).first(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(client_id=request.client.client_id,
                                 user_id=request.user.id)
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok

@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = User.query.filter_by(username=username).first()
    if user.check_password(password):
        return user
    return None

@app.route('/api/authorize', methods=['POST'])
@require_login
@oauth.authorize_handler
def authorize(*args, **kwargs):
    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'

@app.route('/api/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return None

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

class Species(db.Model):
    id = db.Column(Integer, primary_key=True)
    scientific_name = db.Column(String(50))
    name = db.Column(String(50))
    family = db.Column(String(50))
    description = db.Column(Text)
    s_type = db.Column(String(20))
    image = db.Column(String(999))

    def __init__(self, scientific_name: str, image:str, name: str, family: str, description: str, s_type: str):
        self.scientific_name = scientific_name
        self.name = name
        self.family = family
        self.image=image
        self.description = json.dumps(description) if description is not None else None
        self.s_type = s_type

    def toDict(self):
        return {
            "s_name": self.scientific_name, 
            "name": self.name, 
            "family": self.family, 
            "id":self.id,
            "description": json.loads(self.description) if self.description is not None else None, 
            "type": self.s_type,
            "image":self.image
        }    

    def toDictPure(self):
        return {
            "scientific_name": self.scientific_name, 
            "name": self.name, 
            "family": self.family, 
            "id":self.id,
            "description": self.description, 
            "s_type": self.s_type,
            "image":self.image
        }

    def __repr__(self):
        return f'<Species {self.scientific_name}>'


with app.app_context():
    db.create_all()

def toList(scalar):
    list = []
    for item in scalar:
        list.append(item.toDict())
    return list

    
@app.route("/api/mobile/analyze", methods=["POST"])
def analyzeMobile():
    check = checks(request.json)
    res = {"detections":[], "fishes":{}}
    if check[0]:
        contentDecode = check[1]
        if MOBILE_AI == "IMERIR":
            results = imerir_controller.get_labels(contentDecode)
        """else:
            results = vision_controller.get_labels(contentDecode)"""    
        made = []   
        fishes = {}
        for result in results:
            if result["detection"] not in made:
                made.append(result["detection"])
                detail = toList(db.session.execute(
                select(Species).where(Species.name == result["detection"])).scalars())
                if(len(detail)):
                    fishes[detail[0]["name"]] = detail[0]
                    res["detections"].append(result)
        res["fishes"] = fishes
    else:
        return check[1]
    return OK(res)

@app.route("/api/tablet/analyze", methods=["POST"])
def analyzeTablet():
    check = checks(request.json)
    res = {"detections":[], "fishes":{}}
    if check[0]:
        contentDecode = check[1]
        results = imerir_controller.get_labels(contentDecode)
        made = []   
        fishes = {}
        for result in results:
            if result["detection"] not in made:
                made.append(result["detection"])
                detail = toList(db.session.execute(
                select(Species).where(Species.name == result["detection"])).scalars())
                if(len(detail)):
                    fishes[detail[0]["name"]] = detail[0]
                    res["detections"].append(result)
        res["fishes"] = fishes
    else:
        return check[1]
    return OK(results)

@app.route('/api', methods=["GET"])
def hello_world():  # put application's code here
    return OK("hello world!")


@app.route("/api/species", methods=["GET"])
def species_list():
    species = Species.query.all()
    species_serialized = [element.toDict() for element in species]

    return OK(species_serialized)

@app.route("/api/species/<name>")
def speccy(name):
    species = db.session.execute(
        select(Species).where(Species.name == name)).scalars()
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
        image=request.json["image"],
        description=request.json["description"]
    )
    db.session.add(speccy)
    db.session.commit()
    return OK()

@app.route("/api/species_delete/<id>", methods=["DELETE"])
def species_delete(id):
    if(len(toList(db.session.execute(
        select(Species).where(Species.id == id)).scalars())) == 0):
        return BadRequest("FISHNOFOUND")
    db.session.execute(        
        delete(Species).where(Species.id == id)  
    )
    db.session.commit()
    return OK()


@app.route("/api/species_update", methods=["POST"])
def update_species():  
    if(len(toList(db.session.execute(
        db.select(Species).where(Species.id == request.json["id"])).scalars())) == 0):
        return BadRequest("FISHNOFOUND")
    speccy = Species(
        scientific_name=request.json["s_name"],
        name=request.json["name"],
        family=request.json["family"],
        s_type=request.json["type"],
        image=request.json["image"],
        description=request.json["description"]
    )       
    speccy.id=request.json["id"]
    db.session.execute(
        update(Species).values(speccy.toDictPure()).where(Species.id == request.json["id"])   
    )
    db.session.commit()
    return OK()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API")
    parser.add_argument("-p", "--port", default=5000, type=int, help="port number")
    parser.add_argument("-d", "--debug", default=False, type=bool, help="Debug")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port, debug=args.debug)
