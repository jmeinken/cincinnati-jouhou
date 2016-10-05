import json
import pretty

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime

from . import models

@csrf_exempt
def home(request):
    data = "hello world from microfeed"
    return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def get_posts(request):
    uid = int( request.GET.get('uid') )
    last_post_id = int( request.GET.get('last_post_id') )
    post_count = int( request.GET.get('post_count') )
    if last_post_id == 0:
        qPostView = models.PostView.objects.all()[:post_count]
    else:
        qPostView = models.PostView.objects.all().filter(id__lt=last_post_id)[:post_count]
    response = []
    for oPostView in qPostView:
        x = {}
        x['postId'] = oPostView.id
        x['uid'] = oPostView.uid
        x['username'] = oPostView.username
        x['userImage'] = oPostView.user_image
        x['body'] = oPostView.body
        x['date'] = pretty.date( localtime( oPostView.created ).replace(tzinfo=None) )
        if oPostView.uid == uid:
            x['editable'] = True
        else:
            x['editable'] = False
        # append comments
        x['comments'] = []
        qCommentView = models.CommentView.objects.all().filter(post_id=oPostView.id)
        for oCommentView in qCommentView:
            comment = {
                'commentId' : oCommentView.id,
                'uid' : oCommentView.uid,
                'username' : oCommentView.username,
                'userImage' : oCommentView.user_image,
                'body' : oCommentView.body,
                'date' : pretty.date( localtime( oCommentView.created ).replace(tzinfo=None) ),
            }
            if oCommentView.uid == uid:
                comment['editable'] = True
            else:
                comment['editable'] = False
            x['comments'].append(comment)
        response.append(x)
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def get_post(request, post_id):
    data = "get post" + str(post_id)
    return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def new_post(request):
    uid = int( request.POST.get('uid') )
    body = request.POST.get('body').replace('\n', '<br />')
    oPost = models.Post(uid=uid,body=body)
    oPost.save()
    # options = json.loads( request.POST.get('options') )
    oPostView = models.PostView.objects.all().get(id=oPost.id)
    x = {}
    x['postId'] = oPostView.id
    x['uid'] = oPostView.uid
    x['username'] = oPostView.username
    x['userImage'] = oPostView.user_image
    x['body'] = oPostView.body
    x['date'] = pretty.date( localtime( oPostView.created ).replace(tzinfo=None) )
    if oPostView.uid == uid:
        x['editable'] = True
    else:
        x['editable'] = False
    response = x
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def new_comment(request):
    post_id = int( request.POST.get('post_id') )
    uid = int( request.POST.get('uid') )
    body = request.POST.get('body').replace('\n', '<br />')
    oComment = models.Comment(uid=uid,body=body,post_id=post_id)
    oComment.save()
    oCommentView = models.CommentView.objects.all().get(id=oComment.id)
    response = {
        'commentId' : oCommentView.id,
        'postId' : oCommentView.post_id,
        'uid' : oCommentView.uid,
        'username' : oCommentView.username,
        'userImage' : oCommentView.user_image,
        'body' : oCommentView.body,
        'date' : pretty.date( localtime( oCommentView.created ).replace(tzinfo=None) )
    }
    if oCommentView.uid == uid:
        response['editable'] = True
    else:
        response['editable'] = False
    return HttpResponse(json.dumps(response), content_type = "application/json")


@csrf_exempt
def edit_post(request):
    post_id = int( request.POST.get('post_id') )
    body = request.POST.get('body').replace('\n', '<br />')
    oPost = models.Post.objects.all().get(id=post_id)
    oPost.body = body
    oPost.save()
    oPostView = models.PostView.objects.all().get(id=oPost.id)
    x = {}
    x['postId'] = oPostView.id
    x['uid'] = oPostView.uid
    x['username'] = oPostView.username
    x['userImage'] = oPostView.user_image
    x['body'] = oPostView.body
    x['date'] = pretty.date( localtime( oPostView.created ).replace(tzinfo=None) )
    response = x
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def delete_post(request):
    post_id = int( request.POST.get('post_id') )
    oPost = models.Post.objects.all().get(id=post_id)
    oPost.delete()
    response = {
        'postId' : post_id        
    }
    return HttpResponse(json.dumps(response), content_type = "application/json")


@csrf_exempt
def edit_comment(request):
    comment_id = int( request.POST.get('comment_id') )
    body = request.POST.get('body').replace('\n', '<br />')
    oComment = models.Comment.objects.all().get(id=comment_id)
    oComment.body = body
    oComment.save()
    oCommentView = models.CommentView.objects.all().get(id=oComment.id)
    x = {}
    x['commentId'] = oCommentView.id
    x['uid'] = oCommentView.uid
    x['username'] = oCommentView.username
    x['userImage'] = oCommentView.user_image
    x['body'] = oCommentView.body
    x['date'] = pretty.date( localtime( oCommentView.created ).replace(tzinfo=None) )
    response = x
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def delete_comment(request):
    comment_id = int( request.POST.get('comment_id') )
    oComment = models.Comment.objects.all().get(id=comment_id)
    oComment.delete()
    response = {
        'commentId' : comment_id        
    }
    return HttpResponse(json.dumps(response), content_type = "application/json")












