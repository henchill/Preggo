from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	title = models.CharField(max_length = 128)
	content = models.TextField()
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)

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

