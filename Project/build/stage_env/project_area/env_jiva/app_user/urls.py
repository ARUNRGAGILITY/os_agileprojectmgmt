from django.urls import path, include

from . import views as app_user_views

urlpatterns = [
    # user with basic login system
    path('login_page/', app_user_views.login_page, name="login_page"),
    path('logout_page/', app_user_views.logout_page, name="logout_page"),
    path('register_page/',app_user_views.register_page, name="register_page"),
    path('profile/',app_user_views.profile, name="profile"),
    path('password_change/', app_user_views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('user_home/', app_user_views.user_home, name="user_home"),
    path('user_settings/', app_user_views.user_settings, name="user_settings"),
]
