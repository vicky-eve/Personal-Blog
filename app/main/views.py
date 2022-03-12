from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from flask_login import login_required,current_user
from models import User, Blog, Quote,Subscribe
from .forms import UpdateProfile,BlogForm,CommentForm,UpdateBlog,SubscribeForm
from ..request import get_quotes


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    post = Blog.query.filter_by(user = current_user).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,post=post)

@main.route('/')
def index():
    blogs = Blog.query.all()
    quotes = get_quotes()
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data

        new_subscriber=Subscribe(email=email)
        new_subscriber.save_subscriber()
        flash('Successfull subscription!')
        return redirect(url_for('main.index'))
    
    return render_template('index.html', blogs = blogs,quotes =quotes,user=current_user, form = form)