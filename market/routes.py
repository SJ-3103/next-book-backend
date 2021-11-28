import os
from flask import send_from_directory
from market import app

from market.controller import home, details, books, login, logout, register


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/<book_type>', methods=['GET'])
def handle_home(book_type):
    return home(book_type)


@app.route('/api/detail', methods=['GET'])
def handle_detail():
    return details()


@app.route('/api/nextbook', methods=['GET'])
def handle_send():
    return books()


@app.route('/api/login', methods=['POST', 'GET'])
def handle_login():
    return login()


@app.route('/api/register', methods=['POST'])
def handle_register():
    return register()


@app.route('/api/logout', methods=['GET'])
def handle_logout():
    return logout()
