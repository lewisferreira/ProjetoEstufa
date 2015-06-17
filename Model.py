from myServer import db

class Estufa(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(100))
	local = db.Column(db.String(100))
	meds = db.relationship('Measure')

class Measure(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	est_id = db.Column(db.Integer, db.ForeignKey('Estufa.id'))
	temp = db.Column(db.Float)
	umi = db.Column(db.Float)
