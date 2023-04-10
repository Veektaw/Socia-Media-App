from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('likes', views.likes, name='likes'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('upload', views.upload, name='upload'),
    path('profile/<str:pk>', views.profile, name='profile'),
]