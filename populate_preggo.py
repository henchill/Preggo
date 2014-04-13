import os

def populate():

	add_post(title="My first Post",
		content="more information about my new post")

	add_post(title="My Second Post",
		content="some info about my other post...whoohoo")

	add_comment(post="My first Post",
		content="this is stupid")

def add_post(title, content):
	p = Post.objects.get_or_create(title=title, content=content)
	return p

def add_comment(post, content):
	p = Post.objects.get_or_create(title=post)[0]
	c = Comment.objects.get_or_create(post=p, content=content)
	return c

if __name__ == '__main__':
	print "Starting preggo pupulation script"
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cccolon_project.settings')
	from preggo.models import Post, Comment
	populate()


