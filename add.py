import bcrypt
import pymysql

connection = pymysql.connect(host='localhost', user='root', password='12345678', database='SmartTrash', cursorclass=pymysql.cursors.DictCursor)

password = "Admin1234"
salt = bcrypt.gensalt()
pwd = bcrypt.hashpw(password.encode('utf-8'), salt)

with connection:
    with connection.cursor() as cursor:
        
        sql = "INSERT INTO MUser (name,lastname,email,phone, address, position, education, income, utype, bdate, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
        cursor.execute(sql, ("Admin", "Admin", "admin@admin.com", "+525500000001", "", "2", "6", "0", "1", "25.09.2000", pwd))
        cursor.close()
    connection.commit()