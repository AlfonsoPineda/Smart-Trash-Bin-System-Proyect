from flask import Flask, jsonify, request, Response
import pymysql
from flask_cors import CORS, cross_origin
import bcrypt
from bcrypt import hashpw
from datetime import datetime
from datetime import timedelta  
import numpy as np
import jwt

app = Flask(__name__)
CORS(app)

app_pwd = "Qzwxecrvtbynumilop1Q+29112021"

@app.route('/Users', methods=['POST', 'GET'])
def Users():

	if request.method == 'POST' and request.json['petition'] == 'ASignup':


		headers = request.headers
		try:
			decoded_token = jwt.decode(headers['token'], app_pwd, algorithms=["HS256"])
		except e:
			response = jsonify({
				'message': "Token inválido"
			})
			response.status_code = 401
			return response
		if  decoded_token['user']== request.json['email']:
			connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
			with connection:
				with connection.cursor() as cursor:
					sql = "SELECT * FROM DToken WHERE email=%s"
					cursor.execute(sql, (request.json['email']))
					user = cursor.fetchone()
					if user[1] == headers['token'] and user[1] == 1:
						now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						if user['creation'] <= datetime.strptime(now, "%Y-%m-%d %H:%M:%S") <=user['expiration']:
							pass
						else:
							response = jsonify({
								'message': "Token expirado"
							})
							response.status_code = 401
							return response
					else:
						response = jsonify({
							'message': "Token inválido"
						})
						response.status_code = 401
						return response


		_json = request.json
		name = str(_json['name']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		lastname = str( _json['lastname']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		email = str(_json['email']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		phone = str(_json['phone']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		address = str(_json['address']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		position = str(_json['position']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		education = str(_json['education']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		income = str(_json['income']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		utype = str(_json['utype']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		bdte = str(_json['bdte']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
		with connection:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "INSERT INTO MUser (name,lastname,email,phone, address, position, education, income, utype, bdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql, (name, lastname, email, phone, address, position, education, income, utype, bdte))
				cursor.close()
			connection.commit()
			connection.close()

		response = jsonify({
			'message': "El registro fue exitoso"
		})
		response.status_code = 200
		return response
	
	elif request.method == 'POST' and request.json['petition'] == 'USignup':
		_json = request.json

		email = str(_json['email']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		password = str(_json['password']).encode()
		salt = bcrypt.gensalt()
		pwd = bcrypt.hashpw(password, salt)
		connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
		with connection:
			with connection.cursor() as cursor:
				sql = "UPDATE MUser SET password= %s WHERE email = %s"
				cursor.execute(sql, (pwd, email))
				cursor.close()
			connection.commit()
			connection.close()
		response = jsonify({
			'message': "Tu registro fue exitoso"
		})
		response.status_code = 200
		return response

	elif request.method == 'GET':

		headers = request.headers
		try:
			decoded_token = jwt.decode(headers['token'], app_pwd, algorithms=["HS256"])
		except e:
			response = jsonify({
				'message': "Token inválido"
			})
			response.status_code = 401
			return response
		if  decoded_token['user']== headers['user']:
			connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
			with connection:
				with connection.cursor() as cursor:
					sql = "SELECT * FROM DToken WHERE email=%s"
					cursor.execute(sql, (headers['user']))
					user = cursor.fetchone()
					if user['token'] == headers['token'] and decoded_token['type'] == 1:
						now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						if user['creation'] <= datetime.strptime(now, "%Y-%m-%d %H:%M:%S") <=user['expiration']:
							pass
						else:
							response = jsonify({
								'message': "Token expirado"
							})
							response.status_code = 401
							return response
					else:
						response = jsonify({
							'message': "Token inválido"
						})
						response.status_code = 401
						return response
		connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
		with connection:
			with connection.cursor() as cursor:
				sql = "SELECT MUser.name,MUser.lastname,MUser.email,MUser.phone, MUser.address, CPosition.position, CEducation.education, MUser.income, CUserType.utype, MUser.bdate FROM MUser LEFT JOIN CUserType ON CUserType.id = MUser.utype LEFT JOIN CPosition on CPosition.id = MUser.position  LEFT JOIN CEducation on CEducation.id = MUser.education"
				cursor.execute(sql, ())
				users = cursor.fetchall()
				user_res=[]
				print(users)
				for user in users:
					user_ins = {
						'name': user['name'], 
						'lastname': user['lastname'], 
						'email':user['email'], 
						'phone': user['phone'], 
						'address':user['address'], 
						'position':user['position'], 
						'education': user['education'], 
						'income':user['income'], 
						'utype':user['utype'], 
						'bdate':user['bdate']
					}
					user_res.append(user_ins)

		response = jsonify({
			'users': user_res
		})
		response.status_code = 200
		return response

@app.route('/Login', methods=['POST'])
def Login():

	_json = request.json
	email = _json['email']
	passwd = str(_json['password']).encode('utf-8')
	connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
	with connection:
		with connection.cursor() as cursor:
			sql = "SELECT email, password, utype FROM MUser WHERE email=%s"
			cursor.execute(sql, (email))
			user=cursor.fetchone()
			print(user)
			if bcrypt.checkpw(passwd, user['password']):
				token = jwt.encode({"user": email, "type":user['utype']}, app_pwd, algorithm="HS256")
				cursor.close()
			else:
				cursor.close()
				response = jsonify({
					'message': "Credenciales inválidas."
				})
				
				response.status_code = 401
				return response
	connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
	with connection:
		with connection.cursor() as cursor:
			now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			
			sql = "INSERT INTO DToken values(%s,%s,%s,%s)"
			cursor.execute(sql, (email, token, now, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")  ))
			connection.commit()
			cursor.close()
			response = jsonify({
				'token': token
			})
			
			response.status_code = 201
			return response

@app.route('/ValidateToken', methods=['POST'])
def ValidateToken():
	headers = request.headers
	try:
		decoded_token = jwt.decode(headers['token'], app_pwd, algorithms=["HS256"])
	except e:
		response = jsonify({
			'message': "Token inválido"
		})
		response.status_code = 401
		return response
	if  decoded_token['user']== request.json['email']:
		connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)	
		with connection:
			with connection.cursor() as cursor:
				sql = "SELECT * FROM DToken WHERE email=%s"
				cursor.execute(sql, (request.json['email']))
				user = cursor.fetchone()
				if user[1] == headers['token']:
					now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					if user['creation'] <= datetime.strptime(now, "%Y-%m-%d %H:%M:%S") <=user['expiration']:
						response = jsonify({
							'message': "Token válido",
							"is_valid": True
						})
						response.status_code = 200
						return response
					else:
						response = jsonify({
							'message': "Token expirado"
						})
						response.status_code = 401
						return response
				else:
					response = jsonify({
						'message': "Token inválido"
					})
					response.status_code = 401
					return response
	else:
		response = jsonify({
			'message': "Token inválido"
		})
		response.status_code = 401
		return response

@app.route('/Sensor', methods=['POST'])
def Sensor():
	print(request.json)
	response = jsonify({
		'message': "Datos recibidos exitosamente"
	})
	response.status_code = 200
	return response

@app.route('/Containers', methods=['POST', 'GET'])
def Containers():
	
	if request.method == 'POST':

		#Se valida el token
		headers = request.headers
		try:
			decoded_token = jwt.decode(headers['token'], app_pwd, algorithms=["HS256"])
		except e:
			response = jsonify({
				'message': "Token inválido"
			})
			response.status_code = 401
			return response
		if  decoded_token['user']== headers['user']:
			connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
			with connection:
				with connection.cursor() as cursor:
					sql = "SELECT * FROM DToken WHERE email=%s"
					cursor.execute(sql, (headers['user']))
					user = cursor.fetchone()
					if user['token'] == headers['token']:
						now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						if user['creation'] <= datetime.strptime(now, "%Y-%m-%d %H:%M:%S") <=user['expiration']:
							pass
						else:
							response = jsonify({
								'message': "Token expirado"
							})
							response.status_code = 401
							return response
					else:
						response = jsonify({
							'message': "Token inválido"
						})
						response.status_code = 401
						return response

		_json = request.json
		lat = str(_json['lat']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		lng = str( _json['lng']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		fulladdress = str(_json['fulladdress']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		street = str(_json['street']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		urbanity = str(_json['urbanity']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		num = str(_json['num']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		neighborhood = str(_json['neighborhood']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		state = str(_json['state']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		pc = str(_json['pc']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		country = str(_json['country']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		
		name = str(_json['name']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		cont_type = str(_json['type']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "").replace("`", "")
		connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
		with connection:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "INSERT INTO MAddress (lat, lng, fulladdress, street, urbanity, num, neighborhood, state, pc, country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql, (lat, lng, fulladdress, street, urbanity, num, neighborhood, state, pc, country))
				addr_id = cursor.lastrowid
				cursor.close()
			connection.commit()
		connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)

		with connection:
			with connection.cursor() as cursor:
				sql = "INSERT INTO MContainer (name , address, type, capacity ) VALUES (%s,%s,%s, %s)"
				cursor.execute(sql, (name, addr_id, cont_type, "0"))
			connection.commit()

		response = jsonify({
			'message': "El registro fue exitoso"
		})
		response.status_code = 201
		return response

	elif request.method == 'GET':

		headers = request.headers
		try:
			decoded_token = jwt.decode(headers['token'], app_pwd, algorithms=["HS256"])
		except e:
			response = jsonify({
				'message': "Token inválido"
			})
			response.status_code = 401
			return response
		if  decoded_token['user']== headers['user']:
			connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
			with connection:
				with connection.cursor() as cursor:
					sql = "SELECT * FROM DToken WHERE email=%s"
					cursor.execute(sql, (headers['user']))
					user = cursor.fetchone()
					if user['token'] == headers['token']:
						now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						if user['creation'] <= datetime.strptime(now, "%Y-%m-%d %H:%M:%S") <=user['expiration']:
							pass
						else:
							response = jsonify({
								'message': "Token expirado"
							})
							response.status_code = 401
							return response
					else:
						response = jsonify({
							'message': "Token inválido"
						})
						response.status_code = 401
						return response
		connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)
		with connection:
			with connection.cursor() as cursor:
				sql = "SELECT MContainer.id, MContainer.name, MAddress.fulladdress, CContainerType.ctype, MContainer.capacity, MAddress.lat, MAddress.lng FROM MContainer LEFT JOIN MAddress ON MAddress.id = MContainer.address INNER JOIN CContainerType ON CContainerType.id = MContainer.type"
				cursor.execute(sql, ())
				containers = cursor.fetchall()
				cont_res=[]
				print(containers)
				for container in containers:
					cont_ins = {
						'id': container['id'], 
						'name': container['name'], 
						'type':container['ctype'],
						'lat':container['lat'], 
						'lon':container['lng'], 
						'capacity': container['capacity'], 
						'direction': container['fulladdress'], 
					}
					cont_res.append(cont_ins)

		response = jsonify({
			'containers': cont_res
		})
		response.status_code = 201
		return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)