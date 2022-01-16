from market import cursor
from market import connection
import jwt
import datetime

import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path("env\.env"))

import bcrypt

def check_user(data):

    try:
        payload = jwt.decode(
            data,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"]
        )
        email_id = payload['email']

        response = {
            "email_id": email_id
        }
    except jwt.ExpiredSignatureError:
        response = {
            "msg":'Signature expired. Please log in again.'
        }
    except jwt.InvalidTokenError:
        response = {
            "msg":'Invalid token. Please log in again.'
        }
    
    return response


def register_user(data):  # for register

    if data is None:
        return "Please Enter Data."

    first_name = data["first_name"]
    last_name = data["last_name"]
    email_id = data["email_id"]
    password = data["password"]

    # print(bcrypt.gensalt().encode())
    hashed_pwd = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    # print(hashed_pwd)
    
    # check if user is already present or not
    sql = """SELECT email_id FROM Users WHERE email_id=(%s);"""
    
    try:
        cursor.execute(sql,(email_id,))
        
        user = cursor.fetchone()
        
        if user is None:
            # insert user
            sql = """INSERT INTO Users(first_name,last_name,email_id,password) VALUES(%s,%s,%s,%s);"""
            cursor.execute(sql,(first_name,last_name,email_id,hashed_pwd,))
            connection.commit()

            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'email': email_id
            }
            cookie =  jwt.encode(
                payload,
                os.getenv("SECRET_KEY")
            )

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


def login_user(data):  # for login

    email_id = data["email_id"]
    password = data["password"]

    try:
        sql = """SELECT email_id,password FROM Users WHERE email_id=(%s);"""
        
        cursor.execute(sql,(email_id,))
        user = cursor.fetchone()
        connection.commit()
        
        if user is None:
            response = {
                "msg": "user not fund"
            }
        else:
            if bcrypt.checkpw(password.encode(),user[1].encode()):
                # print("true")
                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                    'email': email_id
                }
                cookie =  jwt.encode(
                    payload,
                    os.getenv("SECRET_KEY")
                )
                response = {
                    "msg": "user found",
                    "cookie": cookie
                }
            else:
                # print("false")
                response = {
                    "msg": "password is wrong"
                }

        return response

    except Exception as e:
        print(e)
