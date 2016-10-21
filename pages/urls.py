from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    
    url(r'^new', views.new_page, name='new_page'),
    url(r'^edit/(?P<page_id>[0-9]+)', views.edit_page, name='edit_page'),
    url(r'^view/(?P<page_id>[0-9]+)', views.page, name='page'),
    url(r'^list/(?P<category>[a-z]+)', views.list, name='list'),
]