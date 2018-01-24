from __future__ import unicode_literals
from django.db import models

import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_registration_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []
        # check length of name fields
        if len(post_data['first_name']) < 2:
            errors.append("First name must be at least 2 characters long")
        if len(post_data['last_name']) < 2:
            errors.append("Last name must be at least 2 characters long")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("Password must be at least 8 characters long")
        # check name fields for letter characters
        if not re.match(NAME_REGEX, post_data['first_name']):
            errors.append('First name may only contain characters')
        if not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('First name may only contain characters')
        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("Invalid email")
        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("Email already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['pw_confirm']:
            errors.append("Passwords do not match!")

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            user = User.objects.create(
                        first_name = post_data['first_name'],
                        last_name  = post_data['last_name'],
                        email      = post_data['email'],
                        user_level = "Normal",                       
                        password   = hashedpwd)

            response['user'] = user
            
            # if this is the first user, then they will be made the admin
            if response['user'].id == 1:
                User.objects.update(user_level="Admin")
        return response

    def validate_login_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []
        hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

        user = User.objects.filter(email = post_data['email'])

        if len(user) > 0:
            # check this user's password
            user = user[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            response['user'] = user
        return response

# Create your models here.
class User(models.Model):
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    email       = models.EmailField(unique=True)
    password    = models.CharField(max_length=255)
    user_level  = models.CharField(max_length=10, default="Normal")
    desc        = models.CharField(max_length=1000, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = UserManager()
    def __str__(self):
        return self.email


# NOTE: With the limited functionality that has been implemented so far,
# the following class definitions work here, but logically and to help
# with extending the functionality in the msg_app, it probably would be
# better to have the Msg and Comment classes in the msg_app

# Users have many messages
class Msg(models.Model):
    text        = models.CharField(max_length=255)
    to_user     = models.ForeignKey (User, related_name="users_msgs")
    from_user_id= models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

# Messages have many comments
class Comment(models.Model):
    text        = models.CharField(max_length=255)
    msg         = models.ForeignKey (Msg, related_name="msgs_comments")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

