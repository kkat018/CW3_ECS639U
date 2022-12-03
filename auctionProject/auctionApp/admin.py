from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AnswerDetails, BidDetails, Item, QuestionDetails, User

admin.site.register(User, UserAdmin)
admin.site.register(Item)
admin.site.register(QuestionDetails)
admin.site.register(BidDetails)
admin.site.register(AnswerDetails)
