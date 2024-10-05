from django.urls import path

from app_loginsystem.mod_auth import views_auth as auth

urlpatterns = [
    path('at_login/', auth.at_login, name="at_login"),
    path('at_register/', auth.at_register, name="at_register"),
    path('at_logout/', auth.at_logout, name="at_logout"),    
    
    # after the user is logged in
    path('user_logged_in/', auth.user_logged_in, name='user_logged_in'),
]