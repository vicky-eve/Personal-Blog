from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from flask_login import login_required,current_user
from models import User, Blog, Quote,Subscribe, Comment
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


@main.route('/comment/<int:blog_id>', methods = ['POST','GET'])
@login_required
def comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    comments = Comment.query.filter_by(blog_id = blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        blog_id = blog_id
        new_comment = Comment(comment = comment,blog_id = blog_id,user=current_user)
        new_comment.save_comment()
        return redirect(url_for('.comment', blog_id = blog_id))
    
    return render_template('comment.html', form = form, blog = blog,comments=comments)

@main.route('/create_new', methods = ['POST','GET'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data         
        new_blog = Blog(title = title,post=post,user=current_user)
        new_blog.save_blog()
        return redirect(url_for('main.index'))
        
    return render_template('new_post.html', form = form,title = "Your Blog"   )