from flask import request, make_response
from market.data import send_books, get_details, get_names_and_id_from_partial_name, print_similar_books
from market.crud import get_cookie,get_user,delete_cookie,insert_user

def home(book_type):
    try:
        data = send_books(book_type)
        return data
    except Exception as e:
        print(e)
        return {"msg": {e}}


def books():
    book_name = request.args.get('book_name')
    if book_name == '':
        print(book_name)
        return {"msg": "name null error"}
    else:
        res_new = print_similar_books(book_name)

        if res_new["msg"] == "Error":
            res_new = get_names_and_id_from_partial_name(book_name)
            return {"msg": "name error", "expected": res_new}
        else:
            return res_new


def details():
    book_id = request.args.get('book_id')
    try:
        res = get_details(book_id)
        return res
    except Exception as e:
        print(e)
        return {"msg": "ERROR"}


def login():
    if request.method == 'GET':
        try:
            jwt_cookie = request.cookies.get('jwt')
            if jwt_cookie:  # cookie found
                user = get_cookie(jwt_cookie)
                response = None
                if user.get("email_id"):
                    response = make_response({
                        "cookie": True,
                        "email_id": user.get("email_id")
                    }, 200)

                elif user.get("msg") == str("cookie not found"):
                    response = make_response({
                        "cookie": False,
                    })
                    response.delete_cookie('jwt')
            else:
                response = make_response({"msg": "No cookie"})

            return response
        except Exception as e:
            return make_response({"msg": e})

    if request.method == 'POST':
        try:
            data = request.json
            res = get_user(data)

            if res.get("msg") == str("user not found"):
                response = make_response({
                    "msg": res.get("msg")
                }, 200)

            elif res.get("msg") == str("user found"):
                response = make_response({
                    "email_id": res.get("email_id")
                }, 200)

                response.set_cookie('jwt', value=res.get('cookie'), httponly=False,
                                    max_age=10 * 24 * 60 * 60, secure=True)

            return response
        except Exception as e:
            return make_response({"msg": e})


def register():
    try:
        data = request.json
        res = insert_user(data)

        if res.get("msg") == str("ok"):
            response = make_response({
                "email_id": data['email_id'],
                "redirect": True
            })
            response.set_cookie('jwt', value=res.get("cookie"), max_age=10 * 24 * 60 * 60,
                                httponly=False, secure=True)
        elif res.get("msg") == str("user already present"):
            response = make_response({
                "msg": res.get("msg")
            })
        else:
            response = None

        return response

    except (Exception, TypeError) as e:
        return make_response({"msg": "error"})


def logout():
    jwt_cookie = request.cookies.get("jwt")

    try:
        res = delete_cookie(jwt_cookie)

        if res.get("msg") == str("Ok"):
            response = make_response({
                "msg": "logout success"
            }, 200)

            response.delete_cookie('jwt')

        elif res.get("msg") == str("error"):
            response = {"msg": "Error"}

        return response
    except Exception as e:
        return make_response({'msg': e})


