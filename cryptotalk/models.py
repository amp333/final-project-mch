from django.db import models
import re

from django.db.models.fields import IntegerField

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postdata['Password']) < 8:
            errors['Password'] = "Your password must be at least 8 characters"
        if len(postdata['fname']) < 2 or len(postdata['lname']) < 2:
            errors['name'] = "Your name must be at least 2 characters"
        if not email_checker.match(postdata['email']):
            errors['email'] = 'Email must be valid'
        if postdata['Password'] != postdata['confPassword']:
            errors['Password'] = 'Password and Confirm Password do not match'
        return errors
        
# USER
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = UserManager()
    # user.user_post
    # user.comments
    # user.liked_posts

# POST
class Crypto_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # post.poster.first_name
    # post.comments

# COMMENT
class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    crypto_message = models.ForeignKey(Crypto_Message, related_name="post_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # comment.user
    # comment.post