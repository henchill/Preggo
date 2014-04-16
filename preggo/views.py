from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from preggo.models import Post, Comment, Question, Answer

from preggo.forms import * #PostForm, CommentForm, QuestionForm, AnswerForm

@login_required
def index(request):
	context = RequestContext(request)
	context_dict = {}
	if (request.user.is_authenticated()):
		post_list = request.user.post_set.all()
		question_list = request.user.question_set.all()
		context_dict['posts']  = post_list
		context_dict['questions'] = question_list

		for post in post_list:
			post.url = post.title.replace(' ', '_')

		for quest in question_list:
			quest.url = quest.title.replace(' ', '_')
		
	return render_to_response('preggo/index.html', context_dict, context)

@login_required
def post(request, post_title_url):
	#request our context form the request passed to us
	context = RequestContext(request)

	# convert url back to title
	post_title = post_title_url.replace('_', ' ')

	# create context dict to be used by template
	context_dict = {'post_title': post_title}

	try:
		post = Post.objects.get(title=post_title)
		post.url = post_title_url
		comments = Comment.objects.filter(post=post)

		context_dict['comments'] = comments

		context_dict['post'] = post

	except Post.DoesNotExist:
		pass

	return render_to_response("preggo/post.html", context_dict, context)

@login_required
def add_post(request):
	# Get the contest from the request.
	context = RequestContext(request)

	# A HTTP Post?
	if request.method == 'POST':
		form = PostForm(request.POST)

		# Have we been provided with a valid form
		if form.is_valid():
			# Save the new post to the database
			post = form.save(commit=False)			
			post.user = request.user
			post.save()

			# Send request to view the index view
			return HttpResponseRedirect('/preggo/')
		else:
			# The form contained an error. Print erros to terminal
			print form.errors
	else:
		# If request wasn't post, show the form
		form = PostForm()			

	# request wasn't a post or form had errors.
	return render_to_response('preggo/add_post.html', {'form': form}, context)

@login_required
def add_comment(request, post_title_url):
	# Get the contest from the request.
	context = RequestContext(request)

	post_title = post_title_url.replace("_", " ")
	# A HTTP Post?
	if request.method == 'POST':
		form = CommentForm(request.POST)

		# Have we been provided with a valid form
		if form.is_valid():
			# Not commiting because not all fields are populated
			comment = form.save(commit=False)

			try:
				postObj = Post.objects.get(title=post_title)
				comment.post = postObj 
			except Post.DoesNotExist:
				return_to_response("/preggo/add_post.html", {}, context)

			comment.save()

			# Send request to view the index view
			return redirect(postObj) #post(request, post_title_url)
		else:
			# The form contained an error. Print erros to terminal
			print form.errors
	else:
		# If request wasn't post, show the form
		form = CommentForm()			

	# request wasn't a post or form had errors.
	return render_to_response('preggo/add_comment.html',
		 {'form': form,
		  'post_title_url': post_title_url,
		  'post_title': post_title}, context)

def signup(request):
	context = RequestContext(request)

	# says if the signup was successful
	registered = False

	if request.method == 'POST':
		# get info from form
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			# hash the password 
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
		'preggo/signup.html',
		{'user_form': user_form, 'profile_form': profile_form,
		 'registered': registered}, context)
	
def user_login(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/preggo/')
			else:
				return HttpResponse("Your account is disabled")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied")
	else:
		return render_to_response('preggo/welcome.html', {}, context)

@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/preggo/')

@login_required
def add_question(request):
	# Get the contest from the request.
	context = RequestContext(request)

	# A HTTP Post?
	if request.method == 'POST':
		form = QuestionForm(request.POST)

		# Have we been provided with a valid form
		if form.is_valid():
			# Save the new post to the database
			question = form.save(commit=False)
			question.user = request.user
			question.save()
			# Send request to view the index view
			return index(request)
		else:
			# The form contained an error. Print erros to terminal
			print form.errors
	else:
		# If request wasn't post, show the form
		form = QuestionForm()			

	# request wasn't a post or form had errors.
	return render_to_response('preggo/add_question.html', {'form': form}, context)

@login_required
def view_question(request, question_title_url):
			#request our context form the request passed to us
	context = RequestContext(request)

	# convert url back to title
	question_title = question_title_url.replace('_', ' ')

	# create context dict to be used by template
	context_dict = {'question_title': question_title}

	try:
		question = Question.objects.get(title=question_title)
		question.url = question_title_url
		answers = Answer.objects.filter(question=question)

		context_dict['answers'] = answers

		context_dict['question'] = question

	except Question.DoesNotExist:
		pass

	return render_to_response("preggo/view_question.html", context_dict, context)

@login_required
def add_answer(request, question_title_url):
	# Get the contest from the request.
	context = RequestContext(request)

	question_title = question_title_url.replace("_", " ")
	# A HTTP Post?
	if request.method == 'POST':
		form = AnswerForm(request.POST)

		# Have we been provided with a valid form
		if form.is_valid():
			# Not commiting because not all fields are populated
			answer = form.save(commit=False)

			try:
				questionObj = Question.objects.get(title=question_title)
				answer.question = questionObj

				answer.user = request.user

			except Question.DoesNotExist:
				return_to_response("/preggo/add_question.html", {}, context)

			answer.save()

			# Send request to view the index view
			return view_question(request, question_title_url)
		else:
			# The form contained an error. Print erros to terminal
			print form.errors
	else:
		# If request wasn't post, show the form
		form = AnswerForm()			

	# request wasn't a post or form had errors.
	return render_to_response('preggo/add_answer.html',
		 {'form': form,
		  'question_title_url': question_title_url,
		  'question_title': question_title}, context)

def medfacts(request):
	context = RequestContext(request)
	return render_to_response('preggo/medfacts.html', {}, context)

@login_required
def forum(request):
	context = RequestContext(request)
	question_list = request.user.question_set.all()
	context_dict = {"questions": question_list}
	return render_to_response('preggo/forum.html', context_dict, context)