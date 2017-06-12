from __future__ import unicode_literals
from django.db import models
import re
NAME_REGEX =re.compile('^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt
# Create your models here.

class UserManager(models.Manager):
	def register(self,postData):
		# return (True)
		if len(postData['username']) < 2 or not NAME_REGEX.match(postData['username']):
			return {'error' : 'No fewer than 2 characters in username and letters only'}
		elif len(postData['email']) < 1:
			return {'error' : 'Email cannot be blank'}
		elif not EMAIL_REGEX.match(postData['email']):
			return {'error' : 'Invalid email format'}
		elif User.objects.filter(email=postData['email']):
			return {'error' : 'Email is already registered'}
		elif len(postData['password']) < 8:
			return {'error' : 'Please enter at least 8 characters of password'}
		# elif User.objects.filter(password=postData['password']):
		# 	return {'error' : 'The password was used'}
		elif postData['confirm_password'] != postData['password']:
			return {'error': 'The password NOT match!'}
		else:
			reg_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
			return {'loginUser' : User.objects.create(username = postData['username'], email = postData['email'], password = reg_pw) }
	
	def login(self, postData):
		if len(postData['email']) < 1:
			return {'error' : 'Email cannot be blank'}
		elif not EMAIL_REGEX.match(postData['email']):
			return {'error' : 'Invalid Format'}
		elif not User.objects.filter(email = postData['email']):
			return {'error' : 'user does not exist.'}
		elif len(postData['password']) < 8:
			return {'error' : 'Please enter at least 8 characters of password'}
		else:
			if User.objects.filter(email = postData['email']):
				db_pw = User.objects.get(email = postData['email']).password
                login_pw = bcrypt.hashpw(postData['password'].encode(), db_pw.encode())
                if login_pw != db_pw:
                    return {'error' : 'Wrong password'}
                else:
                    print "Success login"
                    return { 'loginUser' : User.objects.get(email=postData['email']) }  

class QuoteManager(models.Manager):
	def validate(self, postMessage, userid):
		return 
		if len(postData['author']) < 4:
			return {'error' : 'Quote at least 3 characters'}
		elif len(postData['message']) < 10:
			return {'error' : 'Message at least 10 characters'}
		else:
			return { 'quotation' : Quote.objects.get(author=postData['author']) }
		

	def validate(self, postedSecret, userid):
		if len(postedSecret) < 4 :
			return(False, "Seceret need 4 characters long") 
		try:
			currentuser = User.objects.get(id=userid)
			self.create(secret = postedSecret, author=currentuser)
			return(True, "Your secret successful process!")
		except:
			return(False, "We could not create this secret")


class User(models.Model):
	username = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	dob = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __str__(self):
		return str(self.id) + self.username + self.email + self.password


class Quote(models.Model):
	author = models.ForeignKey(User)
	message = models.CharField(max_length = 1000)
	favourite = models.ManyToManyField(User, related_name="favouritequotes")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = QuoteManager()
	def __str__(self):
		return str(self.id) + self.message 











	





