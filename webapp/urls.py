from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserReigtrationView.as_view(), name="sign-up"),
    path("", LoginView.as_view(), name="sign-in"),
    path("index/", IndexView.as_view(), name="home"),
    path("post/<int:id>/comment/add", add_comment, name="add_comment"),
    path("post/<int:id>/like/add", like_post, name="like-post"),
    path("logout/",sign_out_view,name="sign-out")
]