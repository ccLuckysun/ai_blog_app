from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index_redirect, name='index_redirect'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('blogs', views.all_blogs, name='all_blogs'),
    path('blogs/details', views.blog_details, name='blog_details'),
]
