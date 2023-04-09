from db_con import db


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,
                   unique=True, nullable=False)
    autor = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(195), nullable=False)
    release_date = db.Column(db.Integer(), nullable=True)
    lit_type = db.Column(db.String(64), db.ForeignKey('booktypes.id'),
                         nullable=False)

    def __init__(self, author, title, release_date, lit_type, user_id):
        self.author = author
        self.title = title
        self.release_date = release_date
        self.lit_type = lit_type
        self.user_id = user_id