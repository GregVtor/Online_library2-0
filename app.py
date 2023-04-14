import hashlib

from flask import Flask, render_template, request, make_response
from flask_login import LoginManager
from db_con import db_init

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base2'
app.app_context().push()
db = db_init(app)
login_manager = LoginManager()
login_manager.init_app(app)
secret_key = 'cf1cc4234b428b2ece18cd6f9f9613c6680580e23260c01ca4b66' \
             '89f00af1a4fea69e166169e0c45c8e60112e6dc3e2d5a7a6fbccb78' \
             '261f99b3ae404684f961'

from models import *


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id=user_id).first()


@app.route('/', methods=['GET', 'POST'])
def start_page():
    return render_template('start_page.html')


@app.route('/login', methods=['POST'])
def login_handler():
    if request.json['request_type'] != 'Login':
        res = make_response('invalid request type', 400)
        res.headers['Content-Type'] = 'application/text'
        return res

    email = request.json['email']
    password = request.json['password']

    if not email or not password or not db.session.query(User).filter_by(
            email=email).first():
        res = make_response('invalid login data', 400)
        res.headers['Content-Type'] = 'application/text'
        return res

    hash = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

    if db.session.query(User).filter_by(email=email).first().password != hash:
        res = make_response('invalid login data', 400)
        res.headers['Content-Type'] = 'application/text'
        return res

    return '', 200


@app.route('/register', methods=['POST'])
def register_handler():
    return ''


if __name__ == '__main__':
    app.run(debug=True)
