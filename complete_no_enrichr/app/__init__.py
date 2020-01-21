from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# initialize a Flask object named app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/enrich.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models
from .models import Geneset

def find_or_create_geneset(geneset):
    geneset = "\n".join(sorted(geneset.split()))
    # Get first entry
    geneset_object = Geneset.query.filter_by(geneset=geneset).first()
    if geneset_object == None:
        geneset_object = Geneset(geneset)
        db.session.add(geneset_object)
        db.session.commit()
    return geneset_object

def find_by_id(uid):
    # Get first entry
    geneset_object = Geneset.query.filter_by(uuid=uid).first()
    return geneset_object

# Defines what will happen if the user goes to '/' endpoint
@app.route('/')
def index():
    return render_template("index.html")

# Routing
@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/hello/<name>')
def hello_world(name):
    return render_template("hello.html", name=name)

@app.route('/gene_enrichment', methods=['GET', 'POST'])
@app.route('/gene_enrichment/<string:geneset_id>')
def gene_enrichment(geneset_id=None):
    genes=None
    uid=None
    geneset_object = None
    if geneset_id:
        geneset_object = find_by_id(geneset_id)
    if not geneset_object:
        if request.method == 'GET':
            geneset=request.args.get('genes')
        elif request.method=='POST':
            geneset=request.form.get('genes')
        if geneset:
            geneset_object = find_or_create_geneset(geneset)
    if geneset_object:
        genes = geneset_object.geneset.split("\n")
        uid = geneset_object.uuid
        print(uid)
    return render_template("gene.html", genes=genes, uid=uid)