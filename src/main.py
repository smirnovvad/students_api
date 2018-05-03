from flask import Flask, request, jsonify
import os

from models import db
from schema import ma, StudentSchema, GroupSchema, UserSchema
from urls import urls_blueprint, jwt


app = Flask(__name__)

app.register_blueprint(urls_blueprint)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost:8889/students?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!


jwt.init_app(app)
db.init_app(app)
ma.init_app(app)


if __name__ == '__main__':
    app.run(debug=False)
