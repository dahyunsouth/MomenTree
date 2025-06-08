from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # path('google/login/', views.google_login, name='google-login'),
    # path('google/callback/', views.google_callback, name='google-callback'),

] 