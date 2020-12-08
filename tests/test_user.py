import unittest
from app.models import Blog, User
from app import db


class BlogTest(unittest.TestCase):
    def setUp(self):
        self.user_charles = User(username='ucynthy', password='zion')
        self.new_blog = Blog(id=1, title='Testing', description='Testing testing', blog= 'this is a test blog' user_id=self.user_ucynthy.id)

    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)
    
    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password
    
    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('zion'))
    
    def tearDown(self):
        Blog.query.delete()
        User.query.delete()

    def test_check(self):
        self.assertEquals(self.new_blog.title, 'Testing')
        self.assertEquals(self.new_blog.description, 'Testing testing')
        self.assertEquals(self.new_blog.blog, 'this is a test blog')
        self.assertEquals(self.new_blog.user_id, self.user_ucynthy.id)

    def test_save_blog(self):
        self.new_blog.save()
        self.assertTrue(len(Blog.query.all()) > 0)

    def test_get_blog(self):
        self.new_blog.save()
        blog = Blog.get_blog(1)
        self.assertTrue(blog is not None)
