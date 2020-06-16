import os
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv(verbose=True)

ROOT_PATH = os.environ.get('ROOT_PATH', '/webdev_summer_demo/')
# Load any additional configuration parameters via
#  environment variables--`../.env` can be used
#  for sensitive information!

app = flask.Flask(__name__,
  static_url_path=ROOT_PATH + 'static',
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/enrich.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route(ROOT_PATH + 'static')
def staticfiles(path):
  return flask.send_from_directory('static', path)

@app.route(ROOT_PATH, methods=['GET'])
def index():
    return flask.render_template('index.html')

# Add the rest of your routes....

@app.route(ROOT_PATH + "find", methods=['GET', 'POST'])
@app.route(ROOT_PATH + "find/<name>")
def find(name=None):
    from .model import Tissue, Synonym
    if not name:
      if flask.request.method == 'GET':
        name=flask.request.args.get('name')
      elif flask.request.method=='POST':
        name=flask.request.form.get('name')
    if name:
      tissues = Tissue.query\
        .outerjoin(Synonym, Synonym.tissue_id==Tissue.uuid)\
        .filter((Synonym.synonym == name) | (Tissue.label == name))\
        .all()
      return flask.render_template('find.html', name=name, tissues=tissues)
    
    return flask.render_template('find.html')