from db_con import db


class Bookshelf(db.Model):
    __tablename__ = 'bookshelf'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,
                   unique=True, nullable=False)
    book = db.Column(db.Integer(), db.ForeignKey('book.id'),
                     nullable=False)
    count_all = db.Column(db.Integer(), nullable=False)
    count_issued = db.Column(db.Integer(), nullable=False)
    isbn = db.Column(db.String(17), nullable=False)

    def __init__(self, book, count_all):
        self.book = book
        self.count_all = count_all
        self.count_issued = 0