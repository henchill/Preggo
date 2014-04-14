from django.contrib import admin
from preggo.models import Post, Comment, UserProfile
from preggo.models import Category, Question, Answer

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)