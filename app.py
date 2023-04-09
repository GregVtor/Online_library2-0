from flask import Flask, render_template, request, make_response
from json import dumps

from db_con import db_init

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base2'
app.app_context().push()
db = db_init(app)

from models import *


@app.route('/', methods=['GET'])
def start_page():
    return render_template('start_page.html')


@app.route('/login', methods=['POST'])
def login_handler():
    print(request.json)
    res = make_response(dumps({'mes': 'bad log'}), 400)
    res.headers['Content-Type'] = 'application/json'
    return res


@app.route('/register', methods=['POST'])
def register_handler():
    return ''


if __name__ == '__main__':
    app.run(debug=True)
