import json
import pretty

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime

from . import models
from . import functions


uploads_directory = '/home/ubuntu/django/feed-env/feed/static/uploads/'

@csrf_exempt
def home(request):
    data = "hello world from microfeed"
    return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def get_posts(request):
    currentUid = int( request.GET.get('uid') )
    last_post_id = int( request.GET.get('last_post_id') )
    post_count = int( request.GET.get('post_count') )
    if last_post_id == 0:
        qPost = models.Post.objects.all().order_by('-created')[:post_count]
    else:
        qPost = models.Post.objects.all().filter(id__lt=last_post_id).order_by('-created')[:post_count]
    response = []
    for oPost in qPost:
        x = oPost.objectify(currentUid)
        response.append(x)
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def get_post(request, post_id):
    data = "get post" + str(post_id)
    return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def new_post(request):
    currentUid = int( request.POST.get('uid') )
    images = request.POST.getlist('images[]')
    body = functions.process_post_body( request.POST.get('body') )
    oPost = models.Post(user_id=currentUid,body=body)
    oPost.save()
    if images:
        i = 1
        for image in images:
            imageArr = image.split(',')
            file_name = 'image_' + str(oPost.id) + '_' + str(i) + '.png'
            fh = open(uploads_directory + "post_images/" + file_name, "wb")
            fh.write(imageArr[1].decode('base64'))
            fh.close()
            oPostImage = models.PostImage(post=oPost,image_name=file_name,order=i)
            oPostImage.save()
            i = i + 1
    response = oPost.objectify(currentUid)
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def new_comment(request):
    post_id = int( request.POST.get('post_id') )
    uid = int( request.POST.get('uid') )
    body = functions.process_comment_body( request.POST.get('body') )
    oComment = models.PostComment(user_id=uid,body=body,post_id=post_id)
    oComment.save()
    response = oComment.objectify(uid)
    return HttpResponse(json.dumps(response), content_type = "application/json")


@csrf_exempt
def edit_post(request):
    post_id = int( request.POST.get('post_id') )
    body = request.POST.get('body').replace('\n', '<br />')
    oPost = models.Post.objects.all().get(id=post_id)
    oPost.body = body
    oPost.save()
    response = oPost.objectify(oPost.user.id)
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
    oComment = models.PostComment.objects.all().get(id=comment_id)
    oComment.body = body
    oComment.save()
    response = oComment.objectify(oComment.user.id)
    return HttpResponse(json.dumps(response), content_type = "application/json")

@csrf_exempt
def delete_comment(request):
    comment_id = int( request.POST.get('comment_id') )
    oComment = models.PostComment.objects.all().get(id=comment_id)
    oComment.delete()
    response = {
        'commentId' : comment_id        
    }
    return HttpResponse(json.dumps(response), content_type = "application/json")












