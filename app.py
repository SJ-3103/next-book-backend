from flask import Flask, request, make_response, jsonify
from markupsafe import escape
from data import send_books, print_similar_books, get_details

from flask_cors import CORS

from postgres_database import insert_user, get_user, get_cookie, delete_cookie

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/api/<book_type>', methods=['GET'])
def handle_api(book_type):
    print(book_type)
    try:
        data = send_books(book_type)
        return data
    except Exception as e:
        print(e)
        return {"msg": {e}}


@app.route('/api/detail', methods=['GET'])
def handle_detail():
    book_id = request.args.get('book_id')
    try:
        res = get_details(book_id)
        return res
    except Exception as e:
        print(e)
        return {"msg": "ERROR"}


@app.route('/api/nextbook/<book_name>', methods=['GET'])
def handle_send(book_name):
    if request.method == 'GET':
        try:
            data = print_similar_books(escape(book_name))
            return data
        except Exception as e:
            print(e)
            return {"msg": "ERROR"}
    else:
        return {"msg": "REQUEST ERROR"}


@app.route('/api/login', methods=['POST', 'GET'])
def handle_login():
    if request.method == 'GET':
        try:
            response = None
            jwt_cookie = request.cookies.get('jwt')
            if jwt_cookie is not None:  # cookie found
                print(jwt_cookie)
                user = get_cookie(jwt_cookie)
                print(user.get_json())
                if user.get_json()['email_id'] is not None:
                    response = make_response(jsonify({
                        "cookie": True,
                        "email_id": user.get_json()["email_id"]
                    }))
                elif user.get_json()['msg'] == "Cookie Not Found":
                    response = make_response(jsonify({
                        "cookie": False,
                    }))
                    response.delete_cookie('jwt')

                return response
            else:
                print("No cookie found")
                return {"msg": "No cookie"}
        except Exception as e:
            return jsonify({"msg": e})

    if request.method == 'POST':
        try:
            data = request.json
            res = get_user(data)
            response = None
            if res.get_json()["msg"] == "User not found":
                response = make_response(res, 200)
            elif res.get_json()["msg"] == "User found":
                response = make_response(jsonify({
                    "email_id": res.get_json()["email_id"]
                }), 200)
                response.set_cookie('jwt', value=res.get_json()['cookie'], httponly=False,
                                    max_age=10 * 24 * 60 * 60, secure=True)
            return response
        except Exception as e:
            return {"msg": {e}}


@app.route('/api/register', methods=['POST'])
def handle_register():
    try:
        data = request.json
        res = insert_user(data)

        if res.get_json()['msg'] == str("User registered successfully"):

            response = make_response(jsonify({
                "email_id": res.get_json()['email_id'],
                "redirect": True
            }))
            response.set_cookie('jwt', value=res.get_json()['cookie'], max_age=10 * 24 * 60 * 60,
                                httponly=False, secure=True)

            return response

        elif res.get_json()["msg"] == str("User already exists"):
            print(res.get_json())
            return res

    except (Exception, TypeError) as e:
        return jsonify({"msg": e})


@app.route('/api/logout', methods=['GET'])
def handle_logout():
    jwt_cookie = request.cookies.get('jwt')
    try:
        res = delete_cookie(jwt_cookie)
        if res.get_json()['error'] is not None:
            return {"msg": "Error"}
        else:
            response = make_response(jsonify({
                "msg": "logout success"
            }), 200)
            response.delete_cookie('jwt')
            return response
    except Exception as e:
        return {'msg': e}


if __name__ == "main":
    PORT = 5000
    print('Server in running on port', PORT)
    app.run()
