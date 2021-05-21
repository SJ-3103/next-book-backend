from flask import Flask, request
from markupsafe import escape
from data import most_rated_books, new_books, best_selling, print_similar_books

app = Flask(__name__)


@app.route('/')
def handle_main():
    return "HELLO"


@app.route('/most-rated')
def handle_most_rated():
    return most_rated_books()


@app.route('/new-books')
def handle_new_books():
    return new_books()


@app.route('/best-selling')
def handle_best_selling():
    return best_selling()


@app.route('/send/<book_name>', methods=['GET'])
def handle_send(book_name):
    if request.method == 'GET':
        try:
            data = print_similar_books(escape(book_name))
            return data
        except Exception as e:
            print(e)
            return "ERROR"
    else:
        print("The request cant be handled")


if __name__ == "main":
    PORT = 5000
    print('Server in running on port', PORT)
    app.run()
