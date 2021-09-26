from psycopg2 import connect, DatabaseError
import hashlib
from flask import jsonify

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path('.',"env"))

def connect_fun():
    print("Connecting to the database server......")
    connection = connect(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD")
    )
    return connection


def user_table():
    sql = """CREATE TABLE user_table(
        user_id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email_id VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );"""
    connection = None
    try:
        connection = connect_fun()
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.commit()
    except (Exception, DatabaseError) as e:
        print(e)
    finally:
        connection.close()
        print("Database connection is closed.")


def insert_user(request_data):
    first_name = request_data['first_name'].lower()
    last_name = request_data['last_name'].lower()
    email_id = request_data['email_id'].lower()
    password = hashlib.sha3_512(request_data['password'].encode()).hexdigest()

    sql = """INSERT INTO user_table(first_name,last_name,email_id,password) VALUES(%s,%s,%s,%s);"""
    connection = None
    try:
        connection = connect_fun()
        cursor = connection.cursor()
        cursor.execute(sql, (first_name, last_name, email_id, password))

        cookie = insert_cookie(email_id)

        cursor.close()
        connection.commit()

        response = jsonify({
            "email_id": email_id,
            "cookie": cookie,
            "msg": "User registered successfully"
        })

        return response

    except (Exception, DatabaseError) as e:
        if e.pgcode == '23505':
            return jsonify({
                "msg": "User already exists"
            })
    finally:
        connection.close()
        print("Database connection is closed")


def get_user(request_data):
    email_id = request_data['email_id'].lower()
    password = hashlib.sha3_512(request_data['password'].encode()).hexdigest()

    sql = """SELECT * FROM user_table WHERE email_id=(%s) AND password=(%s);"""
    connection = None
    try:
        connection = connect_fun()
        cursor = connection.cursor()
        cursor.execute(sql, (email_id, password))

        cookie = insert_cookie(email_id)

        data = cursor.fetchone()

        cursor.close()
        connection.commit()
        print(data)
        if data is None:
            return jsonify({'msg': 'User not found'})
        else:
            print(data[3])
            response = jsonify({
                "email_id": data[3],
                "cookie": cookie,
                "msg": "User found"
            })
            return response

    except (Exception, DatabaseError) as e:
        return {'msg': 'Error occurred'}
    finally:
        connection.close()
        print("Database connection is closed")


def cookie_table():
    sql = (
        """
        CREATE TABLE cookie_table (
        cookie_id SERIAL PRIMARY KEY,
        email_id VARCHAR(255) NOT NULL UNIQUE,
        cookie_value VARCHAR(255) NOT NULL UNIQUE
        );
        """
    )
    connection = None
    try:
        connection = connect_fun()
        cursor = connection.cursor()
        cursor.execute(sql)
        # print("Cookie table has been created")
        cursor.close()
        connection.commit()
    except (Exception, DatabaseError) as e:
        print(e)
    finally:
        connection.close()
        print("Database connection is closed")


def insert_cookie(email_id):
    cookie = str(email_id + "my name is shubham")
    cookie_value = hashlib.sha3_512(cookie.encode()).hexdigest()

    sql = """INSERT INTO cookie_table(email_id,cookie_value) VALUES(%s,%s) RETURNING cookie_value;"""
    connection = None
    try:
        connection = connect_fun()
        cursor = connection.cursor()
        cursor.execute(sql, (email_id, cookie_value))
        cookie_value = cursor.fetchone()[0]
        cursor.close()
        connection.commit()
        return cookie_value
    except (Exception, DatabaseError) as e:
        print(e)
        return {"msg": "ERROR"}
    finally:
        connection.close()
        print("Database connection is closed")


def get_cookie(cookie):
    connection = None
    try:
        if cookie is not None:
            sql = """SELECT email_id,cookie_value FROM cookie_table WHERE cookie_value=(%s);"""
            connection = connect_fun()
            cursor = connection.cursor()
            cursor.execute(sql, (cookie,))

            data = cursor.fetchone()
            # print(len(data[1]))
            cursor.close()
            connection.commit()
            response = jsonify({
                "email_id": data[0]
            })

            return response

    except (Exception, DatabaseError) as e:
        print(e)
        return jsonify({'msg': 'Cookie Not Found'})

    finally:
        connection.close()
        print("Database connection is closed")


def delete_cookie(cookie):
    connection = None
    try:
        sql = """DELETE FROM cookie_table * where cookie_value = (%s);"""
        connection = connect_fun()
        cursor = connection.cursor()
        cursor.execute(sql, (cookie,))

        cursor.close()
        connection.commit()
        print("Done")
        return {"msg": "Ok"}
    except (Exception, DatabaseError) as e:
        print(e)
        return {"error": e}
    finally:
        connection.close()
        print("Database connection is closed")
