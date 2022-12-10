from django.urls import path

from auctionApp import views

app_name = 'auctionApp'

urlpatterns = [
    # messages page
    path('', views.index, name='home'),
    # signup page
    path('signup/', views.signup_view, name='signup'),
    # login page
    path('login/', views.login_view, name='login'),
    # logout page
    path('logout/', views.logout_view, name='logout'),
]
