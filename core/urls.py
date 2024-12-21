from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('read-blog/', views.read_blog, name='read_blog'),
    path('accounts/profile/', views.profile, name='profile'),
]