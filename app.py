from flask import Flask, jsonify, request, Response
import pymysql
from flask_cors import CORS, cross_origin
import bcrypt


app = Flask(__name__)
CORS(app)

connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)

@app.route('/Users', methods=['POST', 'GET'])
def Users():
	print(request)
	print(request.json)
	_json = request.json
	if request.method == 'POST' and _json['petition'] == 'ASignup':
		name = str(_json['name']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		lastname = str( _json['lastname']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		email = str(_json['email']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		phone = str(_json['phone']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		address = str(_json['address']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		position = str(_json['position']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		education = str(_json['education']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		income = str(_json['income']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		utype = str(_json['utype']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")
		bdte = str(_json['bdte']).replace("'", "").replace('"', '').replace("<", "").replace(">", "").replace("=", "")

		with connection:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "INSERT INTO `MUser` (`name`,`lastname`,`email`,`phone`, `address`, `position`, `education`, `income`, `utype`, `bdate`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql, (name, lastname, email, phone, address, position, education, income, utype, bdte))
			connection.commit()
			connection.close()

		response = jsonify({
			'message': "Su registro fue exitoso"
		})
		response.status_code = 200
		return response
	
	elif request.method == 'POST' and _json['petition'] == 'USignup':
		email = _json['email']
		password = str(_json['password']).encode()
		salt = bcrypt.gensalt()
		pwd = bcrypt.hashpw(password, salt)

	elif request.method == 'GET':
		pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)