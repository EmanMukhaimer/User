from django.db import models
from datetime import datetime, date
import re
import bcrypt 
from django.contrib import messages
# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['password'])<8:
            errors["password"] = "Passwords must be at least 8."
        if postData['password']!=  postData['conf_pass']:
            errors["conf_pass"] = "Passwords do not match."
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255, default=None)
    password=models.CharField(max_length=255)
    rule=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    description=models.TextField(blank=True)
    objects = UserManager()

def register_new_user(information):
    # include some logic to validate user input before adding them to the database!
    password = information[3]
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
    print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'    
    # be sure you set up your database so it can store password hashes this long (60 characters)
    # make sure you put the hashed password in the database, not the one from the form!
    user=User.objects.create(first_name=information[0],last_name=information[1], email=information[2], password=pw_hash, rule=information[4])  
    return user  

def error_reg(request):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return True
    else:
        
        return False


def all_users():
    return User.objects.all()

def get_user(id):
    return User.objects.get(id=id)

def filter_users_email(value):
    return User.objects.filter(email=value)

def check_if_users_is_admin(value):
    if User.objects.get(id=value) in User.objects.filter(rule="admin"):
        return True
def delete_user_from_model(value):
    User.objects.get(id=value).delete()

# Create your models here.
class Message(models.Model):
    written_to=models.ForeignKey(User, default=None, related_name="messages_written_to", on_delete = models.CASCADE)
    written_by=models.ForeignKey(User, default=None, related_name="messages_written_by", on_delete = models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user=models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    message=models.ForeignKey(Message, related_name="comments", on_delete = models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

def create_message(request):
    written_to=User.objects.get(id=request.POST['user'])
    written_by=User.objects.get(id=request.session['loged_in_user_id'])
    Message.objects.create(written_to=written_to,written_by=written_by,message=request.POST['message'])

def create_comment(request):
    Comment.objects.create(comment=request.POST['comment'],user=User.objects.get(id=request.POST['user']),message=Message.objects.get(id=request.POST['message']))

def del_message(request):
    Message.objects.get(id=request.POST['message']).delete()

def filter_messages_by_written_to(value):
    return Message.objects.filter(written_to=value)

def all_comments():
    return Comment.objects.all()


def update_information(information, id):
    user=get_user(id)
    user.first_name=information[1]
    user.last_name=information[2]
    user.email=information[0]
    user.rule=information[3]
    user.save()

def update_password(request, id):
    user=get_user(id)
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return True
    else:
        user.password=request.POST['password']
        user.save()
        return False
    

def update_description(information, id):
    user=get_user(id)
    user.description=information
    user.save()

