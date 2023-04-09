from db_con import db


class CLasses(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,
                   unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False)

    def __init__(self, name):
        self.name = name