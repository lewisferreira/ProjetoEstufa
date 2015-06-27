from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDatabase.db'
db = SQLAlchemy(app)

from Model import *

@app.route('/')
def homepage():
	return '''Hello World!!<br><br>route [/]:<br><br>\t\
	Outras rotas:<br>[<a href= \"http://localhost:5000/medidas">/medidas</a>]<br>\
	<br>[<a href= \"http://localhost:5000/medida/new">/medida/new</a>]<br>\
	<br>[<a href= \"http://localhost:5000/new_device">/new_device</a>]<br>\
	[<a href= \"http://localhost:5000/check_device/default">/check_device</a>]"'''

@app.route('/medidas', methods = ['GET'])
@app.route('/medidas/<nome>', methods = ['GET'])
def exibir(nome = None):
	if nome == None:
		M = []
		for i in Measure.query.all():
			M.append({'id': i.id, 'est_id': i.est_id, 'temp': i.temp, 'umi': i.umi})
		return json.dumps(M)
	e = Estufa.query.filter_by(nome=nome).first()
	if e is None:
		return jsonify({'status': False, 'estufa': nome, 'comment': 'nao existe'})
	else:
		M = []
		for i in Measure.query.filter_by(est_id = e.id):
			M.append({'id': i.id, 'est_id': i.est_id, 'temp': i.temp, 'umi': i.umi})
		return json.dumps(M)

@app.route('/medida/new', methods = ['POST'])
@app.route('/medida/new/<nome>', methods = ['POST'])
def new_measure(nome = 'default'):
	e = Estufa.query.filter_by(nome = nome).first()
	if e is None:
		return jsonify({'status': False, 'estufa': nome, 'comment': 'nao existe'})
	if not request.json:
		return jsonify({'status': False})
	a = request.get_json()
	m = Measure()
	m.est_id = e.id
	m.temp = a['temp']
	m.umi = a['umi']
	db.session.add(m)
	db.session.commit()
	return jsonify({'status': True})

@app.route('/check_device', methods = ['GET'])
def check_device(nome):
	e  = Estufa.query.filter_by(nome = nome).first()
	if e is None:
		return jsonify({'status': False})
	return jsonify({'status': True, 'estufa': t.id, 'nome': t.nome, 'local':t.local})

@app.route('/new_device', methods = ['POST'])
def new_device():
	if not request.json:
		return jsonify({'status': False})
	a =  request.get_json()
	e = Estufa()
	e.nome = a['nome']
	e.local = a['local']
	t = Estufa.query.filter_by(nome = e.nome).first()
	if t is None:
		db.session.add(e)
		db.session.commit()
		return jsonify({'status': True})
	return jsonify({'status': False, 'estufa': t.id, 'nome': t.nome, 'local':t.local, 'comment': 'ja existe'})
	

if __name__ == '__main__':
	app.run(debug = True)
