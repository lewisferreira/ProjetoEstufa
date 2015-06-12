from myServer import db

class estufa(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	local = db.Column(db.String(100))
	meds = db.relationship('Measures')

class measure(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	est_id = db.Column(db.Integer, db.ForeignKey('estufa.id'))
	temp = db.Column(db.Float)
	umi = db.Column(db.Float)
