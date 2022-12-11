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

    path('api/items/', views.items_api, name='items_api'),

    path('api/item/<int:item_id>/', views.item_api, name='item_api'),

    path('api/addItem/', views.create_item_api, name='add_item_api'),
]
