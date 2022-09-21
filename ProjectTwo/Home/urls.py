from django.urls import path

from . import views

urlpatterns = [
    # profile urls
    path("home/", views.home, name="home"),
    # login urls
    path("login_user/", views.login_user, name="login_user"),
    path("change_password/", views.change_password, name="change_password"),
    path("print_profile/", views.print_profile, name="print_profile"),
]
