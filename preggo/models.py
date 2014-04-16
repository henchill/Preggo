from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 128)
	content = models.TextField()
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)

	def get_absolute_url(self):
		return "/preggo/post/%s" % self.title.replace(' ', '_')

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post)
	content = models.TextField()
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.content

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance
	user = models.OneToOneField(User)

	# additional attributes
	picture = models.ImageField(upload_to='profile_images', blank=True)

	# Override unicode method
	def __unicode__(self):
		return self.user.username

class Category(models.Model):
	PLANNING = "PL"
	PREGGO = "PR"
	NEW_MOM = "NM"
	EXPERIENCED_MOM = "EM"
	choices = (
		(PLANNING, 'Planning'), 
		(PREGGO, 'Preggo'),
		(NEW_MOM, 'New Mom'), 
		(EXPERIENCED_MOM, 'Experienced Mom'))

	name = models.CharField(max_length = 2, 
							choices = choices,
							default = PLANNING)	

	def __unicode__(self):
		return self.name

class Question(models.Model):
	# category = models.ForeignKey(Category)
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 128)
	content = models.TextField()
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title

class Answer(models.Model):
	question = models.ForeignKey(Question)
	user = models.ForeignKey(User)
	content = models.TextField()
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.content