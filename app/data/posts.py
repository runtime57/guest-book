import sqlalchemy as sa
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = "post"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = sa.Column(sa.String, unique=True, nullable=False)
    content = sa.Column(sa.String, unique=False, nullable=False)

    comment = orm.relation("Comment", back_populates="post", cascade="all, delete")

    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"))
    user = orm.relation("User")