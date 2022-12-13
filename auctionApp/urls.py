from django.urls import path

from auctionApp import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'auctionApp'

urlpatterns = [

    path('', views.index, name='home'),

    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('api/items/', views.items_api, name='items_api'),

    path('api/item/<int:item_id>/', views.item_api, name='item_api'),

    path('api/addItem/', views.create_item_api, name='add_item_api'),

    path('api/checkSession/', views.check_user_authenticated),

    path('api/profile/', views.profile_api),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)