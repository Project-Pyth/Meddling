from django.contrib import admin
from accounts.models import Category, File
from accounts.models import Question
from accounts.models import Feedback
# Register your models

admin.site.register(Category)
admin.site.register(File)
admin.site.register(Question)
admin.site.register(Feedback)
