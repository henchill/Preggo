from django.contrib import admin
from preggo.models import Post, Comment, UserProfile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)