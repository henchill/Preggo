from django import forms
from django.contrib.auth.models import User
from preggo.models import * #Post, Comment, UserProfile, Question, Answer

class PostForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter a title")
	content = forms.CharField(widget=forms.Textarea(),help_text="Please enter your question here")
	upvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	downvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	# An inline class to provide additional information on the form.	
	class Meta:
		# Provide an association between the Modelform and a model
		model = Post

class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(), help_text="Please enter your comment here");
	upvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	downvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Comment

		# what fields to include in the form
		fields = ('content', 'upvotes', 'downvotes')

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta: 
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture',)	

class QuestionForm(forms.ModelForm):
	choices = ["Planning", "Pregnant", "Mom"]
	title = forms.CharField(max_length=128, help_text="Question Title")
	# category = forms.ChoiceField(choices=choices)
	content = forms.CharField(widget=forms.Textarea(), help_text="Enter question")
	upvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	downvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Question
		fields = ('title', 'content', 'upvotes', 'downvotes')


class AnswerForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(), help_text="Enter Answer")
	upvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	downvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Answer
		fields = ('content', 'upvotes', 'downvotes')