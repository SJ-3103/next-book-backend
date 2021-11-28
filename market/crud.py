from market import cursor
from market import connection


def get_cookie(data):
    sql = """SELECT cookie,email_id FROM Cookies WHERE cookie=(%s);"""
    try:
        cursor.execute(sql,(data,))
        
        cookie_value = cursor.fetchone()

        if cookie_value is None:
            response = {
                "msg": "cookie not found"
            }
        else:
            response = {
                "email_id": cookie_value[1]
            }
        return response
    except Exception as e:
        print(e)


def insert_user(data):  # for register
    first_name = data["first_name"]
    last_name = data["last_name"]
    email_id = data["email_id"]
    password = data["password"].encode()
    
    # check if user is already present or not
    sql = """SELECT email_id FROM Users WHERE email_id=(%s);"""
    
    try:
        cursor.execute(sql,(email_id,))
        
        user = cursor.fetchone()
        
        if user is None:
            # insert user
            sql = """INSERT INTO Users(first_name,last_name,email_id,password) VALUES(%s,%s,%s,%s);"""
            cursor.execute(sql,(first_name,last_name,email_id,password,))
            
            cookie = email_id.encode()

            # insert cookie
            sql = """INSERT INTO Cookies(email_id,cookie) VALUES(%s,%s);"""
            cursor.execute(sql,(email_id,cookie,))

            connection.commit()

            response = {
                "msg": "ok",
                "cookie": cookie
            }

        elif user[0] == email_id:
            response = {
                "msg": "user already present"
            }
        else:
            response = None
        return response
    except Exception as e:
        print(e)


def get_user(data):  # for login
    email_id = data["email_id"]
    password = data["password"].emncode()

    try:
        sql = """SELECT email_id,password FROM Users WHERE email_id=(%s) AND password=(%s);"""
        cursor.execute(sql,(email_id,password,))
        user = cursor.fetchone()

        if user is None:
            response = {
                "msg": "user not fund"
            }
        else:
            cookie = email_id.encode()
            sql = """INSERT INTO Cookie(email_id,cookie) VALUE(%s,%s);"""
            
            cursor.execute(sql,(email_id,cookie,))
            connection.commit()
            
            response = {
                "msg": "user found",
                "cookie": cookie
            }

        return response

    except Exception as e:
        print(e)


def delete_cookie(data):
    sql = """SELECT cookie FROM Cookies WHERE cookie=(%s);"""
    try:
        cursor.execute(sql,(data,))
        cookie = cursor.fetchone()

        if cookie is None:
            response = {
                "msg": "cookie not found"
            }
        else:
            sql = """DELETE FROM Cookies * WHERE cookie=(%s);"""
            
            cursor.execute(sql,(data,))
            connection.commit()
            
            response = {
                "msg": "ok"
            }
            return response
    except Exception as e:
        print(e)


