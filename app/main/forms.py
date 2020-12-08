from flask_wtf import FlaskForm
from wtforms import StringField, SelectField , TextAreaField , SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Write something about you.',validators=[Required()])
    submit = SubmitField('Save')

class BlogForm(FlaskForm):
    title = StringField('Title',validators =[Required()])
    description = StringField('Description',validators =[Required()])
    blogs = TextAreaField('Your story',validators =[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Share your comment',validators =[Required()])
    submit = SubmitField('Share')

