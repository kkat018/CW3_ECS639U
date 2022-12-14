from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AnswerDetails, BidDetails, Item, QuestionDetails, User


admin.site.register(QuestionDetails)
admin.site.register(BidDetails)
admin.site.register(AnswerDetails)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'date_of_birth', 'city', 'image' ]
    ordering = ['id']
    

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'starting_price', 'description', 'date_posted', 'image', 'user', 'expiry_date']
    ordering = ['id']

