from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, Text
import json
from sqlalchemy.sql import func

#app = Flask(__name__, template_folder='templates')
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aquarium.db"


if __name__ == '__main__':
    app.run()