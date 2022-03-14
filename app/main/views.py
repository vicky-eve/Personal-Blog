from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from flask_login import login_required,current_user
from ..models import User, Blog, Quote,Subscribe, Comment
from .forms import UpdateProfile,BlogForm,CommentForm,UpdateBlog,SubscribeForm
from ..requests import get_quote
from .. import db, photos
from app.email import mail_message

@main.route('/')
def home():
    '''
    View root function that returns index template
    '''
    quotes = get_quote()
    blog_form = BlogForm()
    all_blogs = Blog.query.order_by(Blog.date_posted.desc()).all()
    
    return render_template('index.html', quotes=quotes, blogs = all_blogs)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    post = Blog.query.filter_by(user = current_user).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,post=post)

@main.route('/',methods = ['POST','GET'])
def index():
    blogs = Blog.query.all()
    quotes = get_quote()
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data

        new_subscriber=Subscribe(email=email)
        new_subscriber.save_subscriber()
        mail_message("You're now subscribed","email/subscribe",new_subscriber.email,new_subscriber=new_subscriber)
        flash('Successfull subscription!')
        return redirect(url_for('main.index'))
    
    return render_template('index.html', blogs = blogs,quotes =quotes,user=current_user, form = form)

@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """
         subscribe function that subscribes the user to the post
    """
    email = request.args.get('email')
    new_subscriber = Subscribe(email=email)
    db.session.add(new_subscriber)
    db.session.commit()
    flash('Email submitted successfully', 'success')
    return redirect(url_for('main.index')) 

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
        
    return render_template('new_post.html', form = form,title = "Your Blog")

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data  
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route("/delete_post/<int:blog_id>/delete",methods= ['POST'])
@login_required
def delete_post(blog_id):
    blog_delete = Blog.query.get(blog_id)
    db.session.delete(blog_delete)
    db.session.commit()
    flash('Succsessfully deleted!')
    return redirect(url_for('main.index', blog_id=blog_id))

@main.route("/delete_comment/<int:blog_id>/<int:comment_id>",methods= ['POST'])
@login_required
def delete_comment(comment_id,blog_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    flash('Deleted!')
    return redirect(url_for('.comment', blog_id = blog_id,comment_id=comment_id))

@main.route("/update_post/<int:blog_id>",methods= ['POST','GET'])
@login_required
def update_post(blog_id):
    blog = Blog.query.get(blog_id)
    form = UpdateBlog()
    if form.validate_on_submit():
        blog.title =form.title.data
        blog.post = form.post.data
        db.session.commit()
        flash('Post updated!',)
        return redirect(url_for('main.index',blog_id=blog_id))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.post.data = blog.post
    return render_template('new_blog.html',form=form, title='Update Blog')

@main.route('/recent',methods = ['POST','GET'])
def recent():
    blogs = Blog.query.order_by(Blog.date_posted.desc()).all()
    
    return render_template('recent.html', blogs = blogs)