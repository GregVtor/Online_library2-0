import hashlib
from json import dumps, loads

from flask import Flask, render_template, request, make_response
from flask_login import LoginManager, login_user, login_required, current_user, \
    logout_user

from db_con import db_init

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base2'
app.app_context().push()
db = db_init(app)
login_manager = LoginManager()
login_manager.init_app(app)
BASE_LIST = ['Classes', 'User']
app.secret_key = ';'

from models import Admin, User, Student, Librarian, History, Book, Bookshelf, Teacher, CLasses


def close(self, count):
    session = db.session()
    count_issued = session.query(Bookshelf).filter_by(book=self.book_id).first().count_issued
    if count == self.count:
        self.enable = False
        session.commit()
    else:
        session.query(Bookshelf).filter_by(book=self.book_id).update({'count_issued': count_issued - count})
        self.count -= count
        session.commit()


def user_data(user):
    all_books = []
    session = db.session()
    data = session.query(History).filter_by(user_id=user.id).all()
    for i in data:
        count = i.count
        book_id = i.book_id
        book = db.session.query(Book).filter_by(id=book_id).first()
        name_book = book.title
        author = book.author
        delta = {
            'name': name_book,
            'author': author,
            'count': count,
        }
        all_books.append(delta)
    ret = dumps({'us_name': user.name + ' ' + user.last_name, 'us_class': user.us_class,
                 'all_book': all_books})
    return ret


def get_class_users(class_id):
    sessions = db.session()
    users = sessions.query(Student).filter_by(us_class=class_id).all()
    ret = []
    for i in users:
        data = loads(user_data(i))
        count = 0
        for j in data['all_book']:
            count += j['count']
        ret.append([i.id, i.name, i.last_name, i.email, i.us_class, count])
    return ret


@login_manager.user_loader
def load_user(user_id):
    if db.session.query(Admin).filter_by(id=user_id).first():
        return db.session.query(Admin).filter_by(id=user_id).first()
    if db.session.query(Teacher).filter_by(id=user_id).first():
        return db.session.query(Teacher).filter_by(id=user_id).first()
    if db.session.query(Librarian).filter_by(id=user_id).first():
        return db.session.query(Librarian).filter_by(id=user_id).first()
    return db.session.query(Student).filter_by(id=user_id).first()


@app.route('/', methods=['GET'])
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

    login_user(db.session.query(User).filter_by(email=email).first())
    return '', 200


@app.route('/register', methods=['POST'])
def register_handler():
    if request.json['request_type'] != 'Register':
        res = make_response('invalid request type', 400)
        res.headers['Content-Type'] = 'application/text'
        return res

    email = request.json['email']

    if db.session.query(User).filter_by(email=email).first():
        res = make_response('user with this email already exists', 400)
        res.headers['Content-Type'] = 'application/text'
        return res

    password = hashlib.sha256(bytes(request.json['password'],
                                    encoding='utf-8')).hexdigest()
    name = request.json['name']
    surname = request.json['surname']
    us_class = request.json['class']
    new_user = Student(email, password, name, surname, us_class)
    db_sess = db.session()
    db_sess.add(new_user)
    db_sess.commit()
    login_user(Student)
    return ''


@app.route('/db_req_classes', methods=['GET'])
def db_req_handler():
    classes = db.session.query(CLasses).all()
    classes_names = dumps([[i.id, i.name] for i in classes],
                          ensure_ascii=False)
    res = make_response(classes_names, 200)
    res.headers['Content-Type'] = 'application/json'
    return res


@app.route('/stu', methods=['GET'])
@login_required
def stu():
    if not isinstance(current_user, Student):
        return '', 401
    return ''


@app.route('/stu_d', methods=['GET'])
@login_required
def stu_d():
    if not isinstance(current_user, Student):
        return '', 401
    return user_data(load_user(current_user.id))


@app.route('/lib', methods=['GET'])
# @login_required
def lib():
    # if not isinstance(current_user, Librarian):
    #     return '', 401
    session = db.session()
    classes_list = [i.name for i in session.query(CLasses).all()]
    return render_template('librarian.html')


@app.route('/lib_data_class', methods=['POST'])
@login_required
def lib_data_class():
    if not isinstance(current_user, Librarian):
        return '', 401
    id = request.json['id']
    return get_class_users(id)


@app.route('/log')
def log():
    session = db.session()
    m = session.query(History).filter_by(book_id=1).first()
    close(m, 5)
    session.close()
    logout_user()
    return ''


if __name__ == '__main__':
    get_class_users(1)
    app.run(debug=True)
