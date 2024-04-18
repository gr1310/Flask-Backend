from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, jsonify
from sqlalchemy.engine import create_engine
from sqlalchemy import text
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = db.init_app(app)

################################# HOME ########################################
    
@app.route('/', methods=['GET'])
def server_home():
    return "Server home"