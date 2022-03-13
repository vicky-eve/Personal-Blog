from app.models import Blog,User
from app import db
import unittest

class BlogTest(unittest.TestCase):

    def setUp(self):
        self.user_Victoria = User(username = 'victoria',password = 'awuor', email = 'vicky@gmail.com')
        self.new_blog = Blog(title="Love",post = "Your next relationship is not the last one",user = self.user_Victoria )
            
    def tearDown(self):
        Blog.query.delete()
        User.query.delete()
            
    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.title,"LOve")
        self.assertEquals(self.new_blog.word,"Your next relationship is not the last one")
        self.assertEquals(self.new_blog.user,self.user_Victoria)
        
    def test_save_blog(self):
        self.new_blog.save_review()
        self.assertTrue(len(Blog.query.all())>0)