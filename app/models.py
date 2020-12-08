from . import db,login_manager
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
class User(db.Model,UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email =  db.Column(db.String(255))
    passwd =  db.Column(db.String(255))
    profile_pic =  db.Column(db.String(255))
    bio =  db.Column(db.String(255))
    comments = db.relationship('Comment',backref = 'user',lazy="dynamic")
    blogs = db.relationship('Blog',backref = 'user',lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

        
    @password.setter
    def password(self, password):
        self.passwd = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.passwd,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ ="blogs"
    id = db.Column(db.Integer,primary_key = True)
    blog_title = db.Column(db.String(255))
    blog_description =  db.Column(db.String(255))
    blog_content =  db.Column(db.Text())
    posted = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref = 'blog',lazy="dynamic")

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blog(cls):
        blog = Blog.query.filter_by(id = id).all()
        return blog
    def __repr__(self):
        return f'User {self.blog_title}'

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    blog_id =db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls,blog_id):

        comments= Comment.query.filter_by(blog_id = blog_id).all()
        
        return comments
    
    @classmethod
    def delete_comment(self,blog_id):
        comment= Comment.query.get(blog_id)
        db.session.delete(comment)
        db.session.commit()


    
    def __repr__(self):
        return f'comment: {self.comment}'

class Quote:
    def __init__(self,id,author,quote):
        self.id = id
        self.author = author
        self.quote = quote 


class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(), unique = True)          