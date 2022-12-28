from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserReigtrationView.as_view(), name="sign-up"),
    path("", LoginView.as_view(), name="sign-in"),
    path("index/", IndexView.as_view(), name="home"),
]