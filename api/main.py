from builtins import str

from flask import Flask, request, redirect, url_for, send_from_directory, session
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
import token_utils
from functools import wraps
import roles

app = Flask(__name__, static_url_path='', static_folder="static")
app.secret_key="nbvtobrnjrieqpnvhujl nrsipbnehqsbntrfqsli"

with open("../appconfig.json", "r") as conf:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+json.loads(conf.read())["database"]+".db"

db = SQLAlchemy(app)
db.init_app(app)

MOBILE_AI = "IMERIR"

User, Grant, Role=init(db)

def OK(result="Done"):
    return ({"data": result}, 200)


def KO(err="UNKNW"):
    return ({"error": err}, 500)


def BadRequest(reason="UNKNW"):
    return ({"error": reason}, 400)

def auth(roles=[]):
    def decorator_wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not token_utils.check_token(request):
                return BadRequest("NOTAUTH")
            token = token_utils.decode_auth_token(request.headers.get('Authorization'))
            grants = Grant.query.filter_by(user_id=token["sub"]).all()
            grants = [grant.grant for grant in grants]
            print(grants)
            for role in roles:
                if not token_utils.check_user_grants(token, role) or role not in grants:
                    return BadRequest("NOTGRANT")
            return f(*args, **kwargs)
        return decorated_function
    return decorator_wrapper

@app.route("/admin/auth/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        session["template"]="connection"
        return app.send_static_file("connection/index.html")
    post_data = request.get_json()
    try:
        # fetch the user data
        user = User.query.filter_by(
            username=post_data.get('username'), password=post_data.get('password')
            ).first()
        grants = Grant.query.filter_by(user_id=user.id).all()
        auth_token = token_utils.encode_auth_token(user.id, [grant.grant for grant in grants])
        if auth_token:
            return OK(auth_token)
    except Exception as e:
        print(e)
    return BadRequest("ERRAUTH")

@app.route("/admin/auth/check", methods=["GET"])
def checktoken():
    return OK(token_utils.check_token(request))

@app.route("/admin/dashboard", methods=["GET"])
def dashboard():
    session["template"]="ui"
    file = app.send_static_file('ui/index.html')
    return file

@app.route('/<path:file>')
def send_from_root(file):
    print(session["template"]+'/'+file)
    return app.send_static_file(session["template"]+'/'+file)

@app.route('/js/<path:file>')
def send_js(file):
    return app.send_static_file(session["template"]+'/js/'+file)

@app.route('/css/<path:file>')
def send_css(file):
    return app.send_static_file(session["template"]+'/css/'+file)

@app.route('/fonts/<path:file>')
def send_font(file):
    return app.send_static_file(session["template"]+'/fonts/'+file)

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
    image = db.Column(Text)

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
                else:                    
                    fishes[result["detection"]] = {
                        "description":{},
                        "family":None,
                        "id":-1,
                        "image":None,
                        "name":result["detection"],
                        "s_name":None,
                        "type":"fixed"
                    }
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

@app.route('/', methods=["GET"])
def root():  # put application's code here
    return redirect(url_for("login"))

@app.route("/api")
def api_status():
    return OK({"status":"running"})

@app.route("/api/users", methods=["GET"])
@auth([roles.USER_ACCESS])
def get_all_users():
    return OK([user.toDict() for user in User.query.all()])

@app.route("/api/user/<id>", methods=["POST"])
@auth([roles.USER_UPDATE])
def update_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return BadRequest("NOUSER")
    user.username = request.json["username"] if "username" in request.json else user.username
    return OK()

@app.route("/api/user/<id>", methods=["DELETE"])
@auth([roles.USER_DELETE])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return BadRequest("NOUSER")   
    db.session.execute(        
        delete(User).where(User.id == id)  
    )
    db.session.commit()
    return OK()

@app.route("/api/user", methods=["POST"])
@auth([roles.USER_CREATE])
def create_user(id):
    user = User.query.filter_by(username=request.json["username"]).first()
    if user:
        return BadRequest("USERALEXIST")  
    user = User(
        user=request.json["username"],
        passw=request.json["password"],
    )
    db.session.add(user)
    db.session.commit()
    return OK()

@app.route("/api/species", methods=["GET"])
def species_list():
    species = Species.query.all()
    species_serialized = [element.toDict() for element in species]

    return OK(species_serialized)

@app.route("/api/species/names", methods=["GET"])
def species_names():
    species = Species.query.all()
    species_serialized = [{"name":element.name, "s_name":element.scientific_name} for element in species]

    return OK(species_serialized)
    
@app.route("/api/species/<name>")
def speccy(name):
    species = db.session.execute(
        select(Species).where(Species.name == name)).scalars()
    return OK(species)


@app.route("/api/species/auto_cmp/<tmp_name>")
def autocmpl(tmp_name):
    
    result = db.session.query(Species).filter(Species.name.like('%'+tmp_name+'%'))

    autocomp = []
    for speccy in toList(result):
        autocomp.append(speccy["name"])

    return OK(autocomp)

    # species = db.session.execute(
    #     db.select(Species.name).where(tmp_name in Species.name)).scalars()
    # return OK(toList(species))

@app.route("/api/species_create", methods=["POST"])
@auth([roles.SPECCY_CREATE])
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
@auth([roles.SPECCY_DELETE])
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
@auth([roles.SPECCY_UPDATE])
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
    with open("../appconfig.json", "r") as conf:
        confdoc = json.loads(conf.read())
        parser = argparse.ArgumentParser(description="Flask API")
        parser.add_argument("-p", "--port", default=confdoc["port"], type=int, help="port number")
        parser.add_argument("-d", "--debug", default=confdoc["debug"], type=bool, help="Debug")
    args = parser.parse_args()
    with app.app_context():
        if(User.query.filter_by(username="admin").first() is None):
            user = User("admin", "admin")
            db.session.add(user)
            db.session.commit()

            db.session.add(Role(name=roles.USER_ACCESS, display_name="Access to users"))
            db.session.add(Role(name=roles.USER_UPDATE, display_name="Update a user"))
            db.session.add(Role(name=roles.USER_CREATE, display_name="Create a user"))
            db.session.add(Role(name=roles.USER_DELETE, display_name="Delete a user"))
            db.session.add(Role(name=roles.SPECCY_CREATE, display_name="Create a speccy"))
            db.session.add(Role(name=roles.SPECCY_UPDATE, display_name="Update a speccy"))
            db.session.add(Role(name=roles.SPECCY_DELETE, display_name="Delete a speccy"))
            db.session.commit()

            db.session.add(Grant(user=user.id, name=roles.USER_ACCESS))
            db.session.add(Grant(user=user.id, name=roles.USER_UPDATE))
            db.session.add(Grant(user=user.id, name=roles.USER_CREATE))
            db.session.add(Grant(user=user.id, name=roles.USER_DELETE))
            db.session.add(Grant(user=user.id, name=roles.SPECCY_CREATE))
            db.session.add(Grant(user=user.id, name=roles.SPECCY_UPDATE))
            db.session.add(Grant(user=user.id, name=roles.SPECCY_DELETE))
            db.session.commit()

    app.run(host="0.0.0.0", port=args.port, debug=args.debug)
