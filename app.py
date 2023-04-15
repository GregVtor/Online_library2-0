import hashlib
from json import dumps

from flask import Flask, render_template, request, make_response
from flask_login import LoginManager, login_user

from db_con import db_init

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base2'
app.app_context().push()
db = db_init(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager_admin = LoginManager()
login_manager_admin.init_app(app)
BASE_LIST = ['Classes', 'User']
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

    id = db.session.query(User).filter_by(email=email).first().id

    if db.session.query(Admin).filter_by()
        login_user()

    return '', 200


@app.route('/register', methods=['POST'])
def register_handler():
    return ''


@app.route('/db_req_classes', methods=['GET'])
def db_req_handler():
    classes = db.session.query(CLasses).all()
    classes_names = dumps({'cl': [i.name for i in classes]},
                          ensure_ascii=False)
    res = make_response(classes_names, 200)
    res.headers['Content-Type'] = 'application/json'
    return res


@app.route('/login/admin')



if __name__ == '__main__':
    app.run(debug=True)
