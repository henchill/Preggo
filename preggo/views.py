from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from preggo.models import Post, Comment

from preggo.forms import PostForm, CommentForm

def index(request):
	context = RequestContext(request)
	post_list = Post.objects.order_by('-upvotes')[:5]

	context_dict= {'posts': post_list}

	for post in post_list:
		post.url = post.title.replace(' ', '_')
		
	return render_to_response('preggo/index.html', context_dict, context)

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

def add_post(request):
	# Get the contest from the request.
	context = RequestContext(request)

	# A HTTP Post?
	if request.method == 'POST':
		form = PostForm(request.POST)

		# Have we been provided with a valid form
		if form.is_valid():
			# Save the new post to the database
			form.save(commit=True)

			# Send request to view the index view
			return index(request)
		else:
			# The form contained an error. Print erros to terminal
			print form.errors
	else:
		# If request wasn't post, show the form
		form = PostForm()			

	# request wasn't a post or form had errors.
	return render_to_response('preggo/add_post.html', {'form': form}, context)

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
			return post(request, post_title_url)
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
	