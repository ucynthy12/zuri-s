from flask import render_template,redirect,url_for,abort,request,flash
from . import main 
from .. requests import get_quote
from flask_login import login_required, current_user
from .forms import UpdateProfile , BlogForm , CommentForm,UpdateProfile
from ..models import User, Blog, Comment,Subscriber
from .. import db,photos

@main.route('/')
def index():
    quotes = get_quote()
    return render_template('main/index.html', quotes = quotes)

@main.route('/new_blog', methods = ['POST','GET'])
@login_required
def new_blog():

    form = BlogForm()
   
    if form.validate_on_submit():
  
        new_blog = Blog(blog_title = form.title.data, blog_content = form.blogs.data, blog_description = form.description.data,user_id=current_user._get_current_object().id)
        new_blog.save_blog()
        return redirect(url_for('main.blogs'))
        
    return render_template('main/new_blog.html', form = form)

@main.route('/comment/<blog_id>', methods = ["GET","POST"])
@login_required
def comment(blog_id):
    
    form = CommentForm()
    blogs = Blog.query.get(blog_id)
    comments = Comment.get_comment(blog_id)

    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        new_comment = Comment(comment = comment,  user_id = current_user._get_current_object().id,blog_id = blog_id)
        new_comment.save_comment()

        return redirect(url_for('.comment', blog_id = blog_id))
    
    return render_template('main/comment.html', blog = blogs,current_user = current_user, comment_form = form,comments = comments)

@main.route('/blog/<int:id>/update', methods = ['GET','POST'])
@login_required
def update(id):
    blog = Blog.query.filter_by(id= id).first()
    
    form = BlogForm()
    if form.validate_on_submit():
        blog.blog_title = form.title.data
        blog.blog_description = form.description.data
        blog.blog_content = form.blogs.data
        
        db.session.commit()
        return redirect(url_for('main.blogs', id = id))
    elif request.method == 'GET':
        blog.blog_title = form.title.data
        blog.blog_description = form.description.data
        blog.blog_content = form.blogs.data
    
    return render_template('main/new_blog.html', form=form, id=id)

@main.route('/user/<uname>/blogs', methods = ['GET','POST'])
def user_blog(uname):

    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).all()

    return render_template('profile/blogs.html', user = user, blogs = blogs)

@main.route('/blogs', methods = ["GET","POST"])
def blogs():

    blog = Blog.query.all()
    return render_template('main/blogs.html', blog = blog)

   
@main.route('/blogs/comment/delete/<blog_id>', methods = ['GET', 'POST'])
@login_required
def delete(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete_comment()
    db.session.commit()
    return redirect(url_for('main.blogs'))

    
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    title = f"{uname.capitalize()}'s Profile"

    if user is None:
        abort(404)

    return render_template('profile/profile.html', user=user, title=title)

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

@main.route('/user/<uname>/updateprofilepic',methods= ['POST','GET'])
@login_required
def update_profile_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic = path
        db.session.commit()
        return redirect(url_for('.profile',uname=uname))
    return render_template('profile/updatepic.html')
