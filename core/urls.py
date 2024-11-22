from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("chat/", views.chat, name="chat"),
    path("clear-chat/", views.clear_chat, name="clear_chat"),
]
