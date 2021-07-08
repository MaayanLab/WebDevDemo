from .app import db
from uuid import uuid4

class Enrichment(db.Model):
	uuid = db.Column(db.String(35), primary_key=True)
	signature_name = db.Column(db.String(), unique=True)
	shortId = db.Column(db.String(), unique=False)
	userListId = db.Column(db.String(), unique=True)

	def serialize(self):
		return {
			"signature_name": self.signature_name,
			"shortId": self.shortId,
			"userListId": self.userListId
		}

	def __repr__(self):
		return '<%s>' % self.signature_name

	def __init__(self, signature_name, shortId, userListId):
		# generate uuid
		self.uuid = str(uuid4())
		self.signature_name = signature_name
		self.shortId = shortId
		self.userListId = userListId