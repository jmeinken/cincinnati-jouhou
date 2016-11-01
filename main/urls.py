from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^login', views.login_view, name='login'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^create_account', views.create_account, name='create_account'),
    url(r'^edit_account', views.edit_account, name='edit_account'),
    url(r'^set_english', views.set_english, name='set_english'),
    url(r'^set_japanese', views.set_japanese, name='set_japanese'),
    url(r'^$', views.home, name='home')
]