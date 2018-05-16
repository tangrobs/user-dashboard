from __future__ import unicode_literals
from django.db import models #pylint: disable = E0401

import re
import bcrypt #pylint: disable = E0401
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['f_name_len'] = "First name must be at least 2 characters"
        elif not postData['first_name'].isalpha():
            errors['f_name_alpha'] = "First name must be only letters"
        if len(postData['last_name']) < 2:
            errors['l_name_len'] = "Last name must be at least 2 characters"
        elif not postData['last_name'].isalpha():
            errors['l_name_alpha'] = "Last name must be only letters"
        if len(postData['email']) < 1:
            errors['l_email'] = "Email Cannot be blank!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['inv_email'] = "Invalid Email!"
        elif User.objects.filter(email = postData['email']):
            errors['dupl_email'] = "Email already exists."
        if len(postData['password']) < 8:
            errors['pword_len'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['password_confirm']:
            errors['mm_pword'] = "Passwords do not match"
        if errors:
            return {"error_messages":errors}
        else:
            if not User.objects.all():
                adminFlag = True
            else:
                adminFlag = False
            phash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email = postData['email'], pwhash = phash, admin = adminFlag)



            return {"user":User.objects.last()}
    
    def login_validator(self, postData):
        user = User.objects.filter(email = postData['email'])
        if user:
            if bcrypt.checkpw(postData['password'].encode(),user[0].pwhash.encode()):
                return {"user":user[0]}
            return False
        else:
            return False

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    pwhash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    admin = models.BooleanField()
    objects = UserManager()