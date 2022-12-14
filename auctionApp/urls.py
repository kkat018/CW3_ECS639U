from django.urls import path

from auctionApp import views

app_name = 'auctionApp'

urlpatterns = [

    path('', views.index, name='home'),

    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('api/items/', views.items_api, name='items_api'),

    path('api/item/<int:item_id>/', views.item_api, name='item_api'),

    path('api/item/makeBid', views.make_bid, name='make_bid' ),

    path('api/search/<str:search_input>', views.search, name='search' ),

    path('api/addItem/', views.create_item_api, name='add_item_api'),

    path('api/checkSession/', views.check_user_authenticated),

    path('api/addQuestion/', views.add_question, name='add_question'),

    path('api/renderQuestions/<int:item_id>/', views.render_questions, name='render_questions'),

    # path('api/addAnswer/<int:item_id>/', views.render_questions, name='render_questions'),
]
