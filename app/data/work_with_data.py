from sqlalchemy import update
from werkzeug.security import generate_password_hash
from . import db_session
from . import posts
from . import comments
from . import users

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = BASE_DIR + "/db/guest_book.sqlite"
db_session.global_init(db_path)

session = db_session.create_session()


def get_id(login):
    global session
    if session.query(users.User).filter(users.User.login == login).count() > 0:
        return session.query(users.User).filter(users.User.login == login).one().id
    return 1


def user_exists(id):
    global session
    if session.query(users.User).filter(users.User.id == id).count() > 0:
        return True
    else:
        return False


def get_all_posts():
    global session
    return session.query(posts.Post)


def get_all_comments():
    global session
    return session.query(comments.Comment)


def get_post_by_id(post_id):
    global session
    return session.query(posts.Post).filter(posts.Post.id == post_id).one()


def get_comment_by_id(comment_id):
    global session
    return session.query(comments.Comment).filter(comments.Comment.id == comment_id).one()


def get_user_by_id(user_id):
    global session
    return session.query(users.User).filter(users.User.id == user_id).one_or_none()


def get_user_by_login(user_login):
    global session
    return session.query(users.User).filter(users.User.login == user_login).one()


def get_password(user_id):
    global session
    return session.query(users.User).filter(users.User.login == user_id).one_or_none().password


def add_post(post_title, post_content, user):
    global session
    session.add(posts.Post(title=post_title, content=post_content, user=user))
    session.commit()


def add_comment(post, comment_content, user):
    global session
    my_comment = comments.Comment(content=comment_content, post=post, user=user)
    session.add(my_comment)
    session.commit()


def add_user(new_login, new_password):
    global session
    new_user = users.User(login=new_login, password=generate_password_hash(new_password))
    session.add(new_user)
    session.commit()


def delete_post(post_id):
    global session
    my_post = session.query(posts.Post).filter(posts.Post.id == post_id).one()
    session.delete(my_post)
    session.commit()


def delete_comment(comment_id):
    global session
    my_comment = session.query(comments.Comment).filter(comments.Comment.id == comment_id).one()
    session.delete(my_comment)
    session.commit()


def delete_user(user_id):
    global session
    my_user = session.query(users.User).filter(users.User.id == user_id).one()
    session.delete(my_user)
    session.commit()


def get_all_users_posts(user_id):
    global session
    all_posts = session.query(posts.Post).filter(posts.Post.user_id == user_id)
    return all_posts


def change_post(post_id, new_title, new_content):
    global session
    session.query(posts.Post).filter(posts.Post.id == post_id).update({'title': new_title, 'content': new_content})
    session.commit()


def change_comment(comment_id, new_content):
    global session
    session.query(comments.Comment).filter(comments.Comment.id == comment_id).update({'content': new_content})
    session.commit()
