from app.model import db
## python initp_db.py

# drop database if it exists
db.drop_all()
# create database from models
db.create_all()