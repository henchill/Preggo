from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from preggo.models import Post, Comment, Question, Answer

from preggo.forms import * #PostForm, CommentForm, QuestionForm, AnswerForm
from datetime import datetime

from haystack.management.commands import update_index

@login_required
def index(request):
    context = RequestContext(request)
    posts = Post.objects.all().order_by('-pub_date')
    context_dict = {'posts': posts}
            
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
            post.pub_date = datetime.now()
            post.save()
            
            # add post to query set        
            update_index.Command().handle()
            
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
            comment.pub_date = datetime.now()
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
            password = user.password

            # hash the password 
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

            user = authenticate(username=user.username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/preggo/')
                else:
                    return HttpResponse("Your account is disabled")
            else:
                print "Invalid login details: {0}, {1}".format(user.username, user.password)
            
                return HttpResponse("Invalid login details supplied")
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('preggo/signup.html',
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
    #Is the user clicking Cancel?
    isCancel = request.POST.get("cancel_question",None) == "Cancel"
    if isCancel:
        #Just go to the forum page
        return HttpResponseRedirect('/preggo/forum/')

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
            question.pub_date = datetime.now()
            question.save()
            # Send request to view the index view
            return HttpResponseRedirect('/preggo/forum/')
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
def upvote_question(request):
    context = RequestContext(request)
    quest_id = None
    print "upvote executed"
    if request.method == 'GET':
        quest_id = request.GET['question_id']   
    upvotes = 0
    if quest_id:
        question = Question.objects.get(id=int(quest_id))
        if question:     
                # print "begin update"
            upvotes = question.upvotes + 1
            question.upvotes = upvotes
            question.save()
    return HttpResponse(upvotes)

@login_required
def downvote_question(request):
    context = RequestContext(request)
    quest_id = None
    if request.method == 'GET':
        quest_id = request.GET['question_id']
        
    downvotes = 0
    if quest_id:
        question = Question.objects.get(id=int(quest_id))
        if question:
            downvotes = question.downvotes + 1
            question.downvotes = downvotes
            question.save()
    return HttpResponse(downvotes)
  
@login_required 
def upvote_post(request):
    context = RequestContext(request)
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']   
    upvotes = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:            
            upvotes = post.upvotes + 1
            post.upvotes = upvotes
            post.save()
    return HttpResponse(upvotes)

@login_required
def downvote_post(request):
    context = RequestContext(request)
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']
        
    downvotes = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:
            downvotes = post.downvotes + 1
            post.downvotes = downvotes
            post.save()
    return HttpResponse(downvotes)

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
                answer.pub_date = datetime.now()
                answer.user = request.user

            except Question.DoesNotExist:
                return_to_response("/preggo/add_question.html", {}, context)

            answer.save()

            # Send request to view the index view
            return redirect(questionObj)
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

def forum(request):
        context = RequestContext(request)
        question_list = Question.objects.all()

        for quest in question_list:
                quest.url = quest.title.replace(' ', '_')

        context_dict = {"questions": question_list}
        return render_to_response('preggo/forum.html', context_dict, context)

@login_required
def user_page(request, user_url):
    context = RequestContext(request)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_posts = user.post_set.all()
    all_posts = Post.objects.all()
    picture = user_profile.picture

    for post in all_posts:
            post.url = post.title.replace(' ', '_')
            
    for post in user_posts:
            post.url = post.title.replace(' ', '_') 

    context_dict = {"all_posts": all_posts,
                    "user_posts": user_posts,
                    "picture": picture}
    return render_to_response('preggo/user_page.html', context_dict, context)
    
@login_required
def search(request):
    context = RequestContext(request)
    # we retrieve the query to display it in the template
    form = PostSearchForm(request.GET)
    # we call the search method from the NotesSearchForm. Haystack do the work!
    results = form.search()
    context_dict = {'results' : results}

    response = render_to_response('search/search.html', context_dict, context)    
    return response
