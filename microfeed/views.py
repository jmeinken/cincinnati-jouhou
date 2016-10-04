import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import models

@csrf_exempt
def home(request):
    data = "hello world from microfeed"
    return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def get_posts(request):
    uid = int( request.GET.get('uid') )
    qPostView = models.PostView.objects.all()
    response = []
    for oPostView in qPostView:
        x = {}
        x['postId'] = oPostView.id
        x['uid'] = oPostView.uid
        x['username'] = oPostView.username
        x['userImage'] = oPostView.user_image
        x['body'] = oPostView.body
        x['date'] = str( oPostView.created )
        # append comments
        x['comments'] = []
        qCommentView = models.CommentView.objects.all().filter(post_id=oPostView.id)
        for oCommentView in qCommentView:
            x['comments'].append({
                'commentId' : oCommentView.id,
                'uid' : oCommentView.uid,
                'username' : oCommentView.username,
                'userImage' : oCommentView.user_image,
                'body' : oCommentView.body,
                'date' : str( oCommentView.created ),
            })
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
    x['date'] = str( oPostView.created )
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
        'date' : str( oCommentView.created ),
    }
    return HttpResponse(json.dumps(response), content_type = "application/json")


@csrf_exempt
def edit_post(request, post_id):
    data = "edit " + str(post_id)
    return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def delete_post(request, post_id):
    data = "delete " + str(post_id)
    return HttpResponse(json.dumps(data), content_type = "application/json")


@csrf_exempt
def edit_comment(request, comment_id):
    data = "edit " + str(comment_id)
    return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def delete_comment(request, comment_id):
    data = "delete " + str(comment_id)
    return HttpResponse(json.dumps(data), content_type = "application/json")












