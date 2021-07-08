import os
import math
import flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import requests

load_dotenv(verbose=True)

ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/enrich'
    
ROOT_PATH = os.environ.get('ROOT_PATH', '/webdevdemo/')
# Load any additional configuration parameters via
#  environment variables--`../.env` can be used
#  for sensitive information!

app = flask.Flask(__name__,
  static_url_path=ROOT_PATH + 'static',
)

@app.route(ROOT_PATH + 'static')
def staticfiles(path):
  return flask.send_from_directory('static', path)

@app.route(ROOT_PATH, methods=['GET'])
def index():
    return flask.render_template('index.html')

# Add the rest of your routes....

## Routes and passing variables to the function
@app.route(ROOT_PATH + "hello", methods=['GET', 'POST'])
@app.route(ROOT_PATH + "hello/<string:name>")
def hello(name=None):
    if flask.request.method == 'GET':
      name=flask.request.args.get('name')
    elif flask.request.method=='POST':
      name=flask.request.form.get('name')
    if name:
      return "Hello " + name
    else:
        return "Hello stranger..."

@app.route(ROOT_PATH + "hello2", methods=['GET', 'POST'])
@app.route(ROOT_PATH + "hello2/<string:name>")
def hello2(name=None):
    if flask.request.method == 'GET':
      name=flask.request.args.get('name')
    elif flask.request.method=='POST':
      name=flask.request.form.get('name')

    return flask.render_template('hello.html', name=name)

## Jinja templating
@app.route(ROOT_PATH + "home", methods=['GET'])
def home():
    return flask.render_template('home.html')

## Setting up the database
## But first add Flask-SQLAlchemy in requirements.txt
## Don't forget to install it!
## pip install -r requirements.txt
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/enrich.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
## Next we define our model


## Setting up an API

@app.route(ROOT_PATH + "api/signatures", methods=['GET'])
def get_signatures():
  from .model import Enrichment
  signatures = Enrichment.query.all()
  results = [i.signature_name for i in signatures]
  return flask.jsonify(results)

@app.route(ROOT_PATH + "api/enrichment", methods=['GET', 'POST'])
def get_enrichment(name=None):
  from .model import Enrichment

  signature = None
  library = None
  if flask.request.method == 'GET':
    library=flask.request.args.get('library')
    signature=flask.request.args.get('signature')
  elif flask.request.method=='POST':
    library=flask.request.form.get('library')
    signature=flask.request.form.get('signature')
  if signature == None:
    return flask.abort(400)
  if library == None:
    library = "GO_Biological_Process_2021"
  print(library)
  query = Enrichment.query
  query = query.filter(Enrichment.signature_name == signature)
  
  enrichment = query.first()
  if enrichment == None:
    return flask.abort(404)
  else:
    userListId = enrichment.userListId
    
    query_string = '?userListId=%s&backgroundType=%s'
    res = requests.get(
        ENRICHR_URL + query_string % (userListId, library)
    )
    results = res.json()[library][0:20]
    data = []
    for i in results:
      data.append({
        "label": i[1],
        "-log pval": -math.log(i[2])
      })
    return flask.jsonify(data)



@app.route(ROOT_PATH + "search", methods=['GET'])
def landing_page():
  return flask.render_template('enrichment/landing.html')