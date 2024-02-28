import sqlalchemy as sa
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = "comment"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    content = sa.Column(sa.String, nullable=False)
    post_id = sa.Column(sa.Integer, sa.ForeignKey("post.id", ondelete="CASCADE"))
    post = orm.relation("Post")
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"))
    user = orm.relation("User")
