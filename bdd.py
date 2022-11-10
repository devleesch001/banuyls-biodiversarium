from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, Text
import json
from sqlalchemy.sql import func

app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aquarium.db"

db = SQLAlchemy(app)
db.init_app(app)
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
    species = db.session.execute(db.select(Species).order_by(Species.scientific_name)).scalars()
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
if __name__ == '__main__':
    app.run()