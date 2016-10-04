from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    
    url(r'^posts/new', views.new_post, name='new_post'),
    url(r'^posts/edit/(?P<post_id>[0-9]*)', views.edit_post, name='edit_post'),
    url(r'^posts/delete/(?P<post_id>[0-9]*)', views.delete_post, name='delete_post'),
    
    url(r'^posts/comments/new', views.new_comment, name='new_comment'),
    url(r'^posts/comments/edit/(?P<comment_id>[0-9]*)', views.edit_comment, name='edit_comment'),
    url(r'^posts/somments/delete/(?P<comment_id>[0-9]*)', views.delete_comment, name='delete_comment'),
    
    url(r'^posts/(?P<post_id>[0-9]+)', views.get_post, name='get_post'),
    url(r'^posts', views.get_posts, name='get_posts'),
]