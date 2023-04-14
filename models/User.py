from db_con import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,
                   unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    enabled = db.Column(db.Integer(), nullable=False)

    def __init__(self, email, password, name, last_name, shurname,
                 enabled=False):
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        self.shurname = shurname
        self.enabled = enabled

    @staticmethod
    def is_authenticated():
        return True

    def is_enabled(self):
        return self.enabled

    @staticmethod
    def is_anonymous():
        return False

    def get_is(self):
        return self.id


class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer(), db.ForeignKey("user.id"),
                   primary_key=True)
    us_class = db.Column(db.Integer(), db.ForeignKey("classes.id"),
                         nullable=False)

    def __init__(self, email, password, name, last_name, shurname,
                 us_class):
        super().__init__(email, password, name, last_name, shurname)
        self.us_class = us_class


class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer(), db.ForeignKey("user.id"),
                   primary_key=True)

    def __init__(self, email, password, name, last_name, shurname):
        super().__init__(email, password, name, last_name, shurname)


class Librarian(User):
    __tablename__ = 'librarian'
    id = db.Column(db.Integer(), db.ForeignKey("user.id"),
                   primary_key=True)

    def __init__(self, email, password, name, last_name, shurname):
        super().__init__(email, password, name, last_name, shurname, 1)


class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer(), db.ForeignKey("user.id"),
                   primary_key=True)

    def __init__(self, email, password, name, last_name, shurname):
        super().__init__(email, password, name, last_name, shurname, 1)


class ClassroomTeacher(Teacher):
    __tablename__ = 'classroomteacher'
    id = db.Column(db.Integer(), db.ForeignKey("teacher.id"),
                   primary_key=True)
    us_class = db.Column(db.Integer(), db.ForeignKey("classes.id"),
                         nullable=False)

    def __init__(self, email, password, name, last_name, shurname,
                 us_class):
        super().__init__(email, password, name, last_name, shurname)
        self.us_class = us_class