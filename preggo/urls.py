from django.conf.urls import patterns, url
from preggo import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name='index'),
	url(r'^post/(?P<post_title_url>\w+)/$', views.post, name='post'),
	url(r'^add_post/$', views.add_post, name='add_post'),
	url(r'^post/(?P<post_title_url>\w+)/add_comment/$', views.add_comment, name='add_comment' ),
	url(r'^question/(?P<question_title_url>\w+)/$', views.view_question, name='view_question'),
	url(r'^add_question/$', views.add_question, name='add_question'),
	url(r'^question/(?P<question_title_url>\w+)/add_answer/$', views.add_answer, name='add_answer'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^login/$', views.user_login, name="login"),
	url(r'^logout/$', views.user_logout, name="logout"),
	url(r'^medfacts/$', views.medfacts, name="medfacts"),
	url(r'^forum/$', views.forum, name="forum"),
	url(r'^(?P<user_url>\w+)/$', views.user_page, name="user_page"),
	
)
