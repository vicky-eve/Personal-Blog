from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import InputRequired, Email

class UpdateProfile(FlaskForm):
    bio = TextAreaField('About you.',validators =[InputRequired()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    post = TextAreaField('Say your piece', validators=[InputRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment',validators=[InputRequired()])
    submit = SubmitField('Comment')

class UpdateBlog(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    post = TextAreaField('Your piece', validators=[InputRequired()],render_kw={'class': 'form-control', 'rows': 5})
    submit = SubmitField('Submit Blog')
    
class SubscribeForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Email()],render_kw={"placeholder": "Enter your email.."})
    submit = SubmitField('Subscribe')