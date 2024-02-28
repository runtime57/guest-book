import sqlalchemy as sa
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    comment = orm.relation("Comment", back_populates="user", cascade="all, delete")
    post = orm.relation("Post", back_populates="user", cascade="all, delete")

    def check_user(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return int(self.id)
