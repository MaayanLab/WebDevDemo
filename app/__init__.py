from flask import Flask
# from flask import Flask, render_template, request 
# from flask_sqlalchemy import SQLAlchemy
# import requests as api_requests
# import json

# initialize a Flask object named app
app = Flask(__name__)

#################################################
# 7. DB setup
# Add Flask-SQLAlchemy==2.4.1 to Requirements.txt
# and rerun it
# Add from flask_sqlalchemy import SQLAlchemy
# to imports
# refer to models.py
# run initialize_db.py and fill_db.py
#################################################
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/enrich.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# from .models import Geneset

######################
# 1 . FIRST FLASK APP
######################
# Defines what will happen if the user goes to '/' endpoint
@app.route('/')
def index():
    return "I'm having so much fun learning wed dev"

###################
# 2. Routing
###################
# # Note the trailing '/' on your routes
# # /about will work
# @app.route('/about/')
# def about():
#     return "I'm gonna be the very best web developer"

# # /hello/ won't work
# @app.route('/hello')
# def hello_world():
#     return "Hello World!"

#################################################
# 3. Adding variables to routes
# comment out hello_world and uncomment this one
#################################################
# @app.route('/hello/<name>')
# def hello_world(name):
#     return 'Hello %s' % name

###################
# 4. Multiple routing
###################
# @app.route('/gene_enrichment')
# @app.route('/gene_enrichment/<gene>')
# def gene_enrichment(gene=None):
#     if gene:
#         return "Oh %s is an interesting gene" % gene
#     else:
#         return "Oh please enter a gene"


#######################################
# 5. TEMPLATING
# Add render_template to flask imports
# refer to the templates directory
#######################################
# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/about/')
# def about():
#     return render_template("about.html")

# @app.route('/hello/<name>')
# def hello_world(name):
#     return render_template("hello.html", name=name)

# @app.route('/gene_enrichment')
# @app.route('/gene_enrichment/<gene>')
# def gene_enrichment(gene=None):
#     genes=None
#     if gene:
#         genes = gene.split()
#     return render_template("gene.html", genes=genes)


#######################################
# 6. GETTING REQUEST VARIABLES
# Add request to flask imports
#######################################
# @app.route('/gene_enrichment', methods=['GET', 'POST'])
# @app.route('/gene_enrichment/<string:gene>')
# def gene_enrichment(gene=None):
#    genes=None
#    if request.method == 'GET':
#        gene=request.args.get('genes')
#    elif request.method=='POST':
#        gene=request.form.get('genes')
#    if gene:
#        genes = gene.split()
#    return render_template("gene.html",
#            genes=genes)

########################################
# 8. Interacting with the database
# Add from .models import Geneset
# to imports.
# Do this after db declaration. Why?
# Querying and insertion
# Suppose we want to add genesets to DB
# Refer to templates/gene.html
########################################
# def find_or_create_geneset(geneset):
#     geneset = "\n".join(sorted(geneset.split()))
#     # Filter table and get the first entry
#     geneset_object = Geneset.query.filter_by(geneset=geneset).first()
#     # Generate a new entry if it does not exist
#     if geneset_object == None:
#         geneset_object = Geneset(geneset)
#         db.session.add(geneset_object)
#         db.session.commit()
#     return geneset_object

# def find_by_id(uid):
#     # Filter table based on uid
#     geneset_object = Geneset.query.filter_by(uuid=uid).first()
#     return geneset_object

# @app.route('/gene_enrichment', methods=['GET', 'POST'])
# @app.route('/gene_enrichment/<string:geneset_id>')
# def gene_enrichment(geneset_id=None):
#     genes=None
#     uid=None
#     geneset_object = None
#     if geneset_id:
#         geneset_object = find_by_id(geneset_id)
#     if not geneset_object:
#         if request.method == 'GET':
#             geneset=request.args.get('genes')
#         elif request.method=='POST':
#             geneset=request.form.get('genes')
#         if geneset:
#             geneset_object = find_or_create_geneset(geneset)
#     if geneset_object:
#         genes = geneset_object.geneset.split("\n")
#         uid = geneset_object.uuid
#     return render_template("gene.html", genes=genes, uid=uid)

#############################################
# 9. Interacting with Enrichr
# Add requests==2.22.0 to Requirements.txt
# Two additional imports:
# import requests as api_requests
# import json
# modify templates/gene.html
############################################
# @app.route('/gene_enrichment', methods=['GET', 'POST'])
# @app.route('/gene_enrichment/<string:geneset_id>')
# def gene_enrichment(geneset_id=None):
#     # API Links
#     ENRICHR_URL_ADD_LIST = 'https://amp.pharm.mssm.edu/Enrichr/addList'
#     ENRICHR_ENRICH_LINK = "https://amp.pharm.mssm.edu/Enrichr/enrich"
#     enrichr_link = ENRICHR_ENRICH_LINK
#     genes=None
#     uid=None
#     geneset_object = None
#     if geneset_id:
#         geneset_object = find_by_id(geneset_id)
#     if not geneset_object:
#         if request.method == 'GET':
#             geneset=request.args.get('genes')
#         elif request.method=='POST':
#             geneset=request.form.get('genes')
#         if geneset:
#             geneset_object = find_or_create_geneset(geneset)
#     # Enrichr 
#     if geneset_object:
#         # Format data for posting to enrichr
#         payload = {
#             'list': (None, geneset_object.geneset),
#             'description': (None, "geneset demo")
#         }
#         response = api_requests.post(ENRICHR_URL_ADD_LIST, files=payload)
#         if response.ok:
#             data = json.loads(response.text)
#             genes = geneset_object.geneset.split("\n")
#             uid = geneset_object.uuid
#             enrichr_link=enrichr_link+"?dataset="+data["shortId"]

#     return render_template("gene.html",
#             genes=genes,
#             uid=uid,
#             enrichr_link=enrichr_link)