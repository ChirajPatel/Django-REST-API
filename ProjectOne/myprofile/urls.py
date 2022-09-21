from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views
from .views import GeneratePdf

urlpatterns = [
    # profile apis url
    path("profiles/", views.profiles, name="profiles"),
    path("profile_delete/", views.profile_delete, name="profile_delete"),
    path("profile_edit_details/", views.profile_edit_details, name="profile_edit_details"),
    path("profile_save/", views.profile_save, name="profile_save"),
    path("change_password/", views.change_password, name="change_password"),
    path("pdf/", GeneratePdf.as_view()),
    path("profile_authentication/", views.profile_authentication, name="profile_authentication"),
    path("api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
