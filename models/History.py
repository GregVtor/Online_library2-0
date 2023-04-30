from db_con import db
from . import Bookshelf
from datetime import datetime


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True,
                   nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    enable = db.Column(db.Boolean, nullable=False)
    data = db.Column(db.String, nullable=False)

    def __init__(self, user_id, book_id, count):
        self.user_id = user_id
        self.book_id = user_id
        self.enable = False
        self.count = count
        self.data = str(datetime.now())
        session = db.session()
        count_issued = session.query(Bookshelf).filter_by(book_id=book_id).first().count_issued
        session.query(Bookshelf).filter_by(book_id=book_id).update().values(count_issued=(count_issued + count))
        session.commit()


