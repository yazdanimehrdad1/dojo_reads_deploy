from django.db import models
from datetime import datetime
import re, bcrypt
# Create your models here.
# EMAIL_REGEX = re.compile(r'^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator_registration(self, postData):
        errors = {}
        already_exist = User.objects.filter(email=postData['email']) #?
        if len(postData['first_name'])<2:
            errors['first_name']  = "first name must be more than 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name']  = "last name must be more than 2 characters"
        if len(postData['password'])<6:
            errors['password'] = "password must be atleas 6 characters"
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Paswords do not match"

        if len(postData['email'])<1:
            errors['email'] = "email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        elif already_exist:
            errors['email'] = "email already exist"
        return errors

    def validator_login(self, postData):
        errors={}
        check_user_exist = User.objects.filter(email = postData['email'])
        if not check_user_exist:
            errors['login_email'] = "You are not registered"
        else:
            if not bcrypt.checkpw( postData['password'].encode() , check_user_exist[0].password.encode() ):
                errors['login_email'] = "Wrong password"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password=models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = UserManager()



class AuthorManager(models.Manager):
    def basic_validator(self, postData):
        errors ={}

        if len(postData['author_name'])<1:
            errors['author_name'] = 'Author name should be at least two characters.'
        return errors

class Author(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AuthorManager()

class BookManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        try:
            Book.objects.get(title = post_data['title'])
            errors['title'] = 'A book with this title already exists!'
        except:
            pass
        if len(post_data['title']) < 1:
            errors['title'] = 'Book title should be at least two characters.'
        return errors

class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(Author, related_name = "books", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class ReviewManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['review']) < 10:
            errors['review'] = 'Review should be at least ten characters long.'
        if int(post_data['rating']) < 1 or int(post_data['rating']) > 5:
            errors['rating'] = 'Review should be 1 to 5 stars.'
        return errors
        
class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    book = models.ForeignKey(Book, related_name = "reviews", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewManager()
