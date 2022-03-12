from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import InputRequired

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