from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDatabase.db'
db = SQLAlchemy(app)

from Model import *

@app.route('/')
def homepage():
	return "Hello World!!<br><br>route [/]:<br><br>\t\
	Outras rotas:<br>[<a href= \"http://127.0.0.1:5000/exibeMedidas/\">/exibeMedidas</a>]<br>\
	[<a href= \"http://127.0.0.1:5000/+medida/\">/+medida</a>]"

@app.route('/exibeMedidas/', methods = ['GET'])
def exibir():
	M = []
	for i in measure.query.all():
		print(i.id, i.est_id, i.temp, i.umi)
		M.append({'id': i.id, 'est_id': i.est_id, 'temp': i.temp, 'umi': i.umi})
	return json.dumps(M)

@app.route('/+medida/', methods = ['POST'])
def new_measure():
	if not request.json:
		return jsonify({'status': False})
	a = request.get_json()
	m = Measure()
	m.est_id = a['est_id']
	m.temp = a['temp']
	m.umi = a['umi']
	db.session.add()
	db.session.commit()
	return jsonify({'status': True})


if __name__ == '__main__':
	app.run()
