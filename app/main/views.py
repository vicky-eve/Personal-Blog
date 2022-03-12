from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from models import User, Blog

@main.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username = username).first()
    post = Blog.query.filter_by(user = current_user).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,post=post)