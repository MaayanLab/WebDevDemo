from .app import db
from uuid import uuid4

class Tissue(db.Model):
    uuid = db.Column(db.String(35), primary_key=True)
    class_id = db.Column(db.String(), unique=True)
    label = db.Column(db.String(), nullable=False)
    definition = db.Column(db.String(), default='')
    synonyms = db.relationship('Synonym', backref='tissue', lazy=True)

    def __repr__(self):
        return '<%s>' % self.class_id
    
    def __init__(self, class_id, label, definition):
        # generate uuid
        self.uuid = str(uuid4())
        self.class_id = class_id
        self.label = label
        self.definition = definition
        

class Synonym(db.Model):
    uuid = db.Column(db.String(35), primary_key=True)
    tissue_id = db.Column(db.String(35), db.ForeignKey('tissue.uuid'),
        nullable=False)
    synonym = db.Column(db.String())
    
    def __repr__(self):
        return '<%s>' % self.synonym
    
    def __init__(self, tissue_id, synonym):
        # generate uuid
        self.uuid = str(uuid4())
        self.tissue_id = tissue_id
        self.synonym = synonym