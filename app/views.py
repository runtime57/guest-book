from flask import render_template, request, flash, redirect, url_for
from app import app
from app.data import work_with_data
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.data import users
from flask_wtf import FlaskForm
from app.data import comments
from app.data import posts

from app.forms.LoginForm import LoginForm

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    posts = work_with_data.get_all_posts()
    comments = work_with_data.get_all_comments()
    if current_user.is_active:
        return render_template("index.html",
                           titile="Home",
                           user=current_user,
                           posts=posts,
                           comments=comments
        )
    else:
        return render_template("index.html",
                               titile="Home",
                               posts=posts,
                               comments=comments
                               )


#добавить пост
@app.route('/add_post', methods=["GET"])
@login_required
def add_post_page():
    return render_template("add_post.html", page_name="add_post")


@app.route('/api/add_post', methods=["POST"])
@login_required
def add_post():
    work_with_data.add_post(request.form['title'], request.form['content'], current_user)
    return redirect('/')


#добавить коммент
@app.route('/add_comment/<int:post_id>', methods=["GET"])
@login_required
def add_comment_page(post_id):
    return render_template("add_comment.html", page_name="add_comment", post=work_with_data.get_post_by_id(post_id))


@app.route('/api/add_comment/<int:post_id>', methods=["POST"])
@login_required
def add_comment(post_id):
    work_with_data.add_comment(work_with_data.get_post_by_id(post_id), request.form['content'], current_user)
    return redirect('/')


# удалить коммент
@app.route('/api/delete_comment/<int:comment_id>', methods=["GET"])
@login_required
def delete_comment(comment_id):
    comment = work_with_data.get_comment_by_id(comment_id)
    if comment.user != current_user:
        return redirect('/wrong_user')
    work_with_data.delete_comment(comment_id)
    return redirect('/')


# удалить пост
@app.route('/api/delete_post/<int:post_id>', methods=["GET"])
@login_required
def delete_post(post_id):
    post = work_with_data.get_post_by_id(post_id)
    if post.user != current_user:
        return redirect('/wrong_user')
    work_with_data.delete_post(post_id)
    return redirect('/')


# обновить пост
@app.route('/update_post/<int:post_id>', methods=["GET"])
@login_required
def update_post_page(post_id):
    post = work_with_data.get_post_by_id(post_id)
    if post.user != current_user:
        return redirect('/wrong_user')
    return render_template('update_post.html', post=work_with_data.get_post_by_id(post_id))


@app.route('/api/update_post/<int:post_id>', methods=["POST"])
@login_required
def update_post(post_id):
    work_with_data.change_post(post_id, request.form['title'], request.form['content'])
    return redirect('/')


# обновить коммент
@app.route('/update_comment/<int:comment_id>', methods=["GET"])
@login_required
def update_comment_page(comment_id):
    comment = work_with_data.get_comment_by_id(comment_id)
    if comment.user != current_user:
        return redirect('/wrong_user')
    return render_template('update_comment.html', comment=work_with_data.get_comment_by_id(comment_id))


@app.route('/api/update_comment/<int:comment_id>', methods=["POST"])
@login_required
def update_comment(comment_id):
    comment = work_with_data.get_comment_by_id(comment_id)
    if comment.user != current_user:
        return
    work_with_data.change_comment(comment_id, request.form['content'])
    return redirect('/')


@app.route('/all_posts_of_user/<int:user_id>')
def all_posts(user_id):
    return render_template('all_posts.html',
                           cur_user=current_user,
                           user=work_with_data.get_user_by_id(user_id),
                           posts=work_with_data.get_all_users_posts(user_id),
                           comments=work_with_data.get_all_comments()
                           )

@app.route('/wrong_user')
@login_required
def wrong_user():
    return render_template('wrong_user.html', user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return work_with_data.get_user_by_id(user_id)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_login = form.login.data
        given_password = form.password.data
        password = work_with_data.get_password(user_login)
        remember_me = form.remember_me.data
        user = work_with_data.get_user_by_login(user_login)
        if check_password_hash(password, given_password):
            login_user(user, remember=remember_me)
            print("Success")
            return redirect('/')
        else:
            print("error")
            print(password, given_password)
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def registration():
    form = LoginForm()
    if form.validate_on_submit():
        user_login = form.login.data
        password = form.password.data
        work_with_data.add_user(user_login, password)
        user = work_with_data.get_user_by_login(user_login)
        login_user(user, remember=True)
        print("Success")
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

