import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from feed.functions import validate_form_with_inlines

from feed import functions
from feed.functions import UPLOADS_DIR

from . import models
from . import forms


page_titles = {
    'restaurant' : 'Restaurants',
    'local_destination' : 'Local Destinations',
    'regional_destination' : 'Regional Destinations',
    'housing' : 'Housing',
    'shopping' : 'Shopping',
    'medical' : 'Medical',
    'transportation' : 'Transportation',
    'education' : 'Education',
}


def home(request):
    return HttpResponse("hello world")




@login_required
def new_page(request):
    context = {}
    form = forms.PageForm()
    children = [forms.PageLinkFormSet]
    if request.method == 'POST':
        form, children, is_valid = validate_form_with_inlines(form, children, request.POST)
        if is_valid:
            oPage = form.save(commit=False)
            oPage.user = request.user
            oPage.save()
            for child in children:
                child.instance = oPage
                child.save()
            messages.success(request, 'Page successfully added.')
            return redirect('pages:page', page_id=oPage.id)
    context['form'] = form
    context['children'] = children
    return render(request, 'pages/new_page.html', context)

@csrf_exempt
def delete_page(request):
    page_id = int( request.POST.get('page_id') )
    oPage = models.Page.objects.all().get(id=page_id)
    oPage.delete()
    messages.success(request, 'Page successfully deleted.')
    return redirect('home')


@login_required
def edit_page(request, page_id):
    context = {}
    oPage = get_object_or_404(models.Page, pk=page_id)
    form = forms.PageForm(instance=oPage)
    children = [forms.PageLinkFormSet]
    if request.method == 'POST':
        form, children, is_valid = validate_form_with_inlines(form, children, request.POST, oPage)
        if is_valid:
            oPage = form.save(commit=False)
            oPage.user = request.user
            oPage.save()
            for child in children:
                child.instance = oPage
                child.save()
            messages.success(request, 'Page successfully edited.')
            return redirect('pages:page', page_id=oPage.id)
    else:
        temp_children = []
        for child in children:
            temp_children.append( child(instance=oPage) )
        children = temp_children
    context['form'] = form
    context['children'] = children
    return render(request, 'pages/new_page.html', context)

def page(request, page_id):
    context = {}
    context['upcoming_events'] = functions.get_upcoming_events()
    oPage = models.Page.objects.all().get(pk=page_id)
    context['oPage'] = oPage
    return render(request, 'pages/page.html', context)

def list(request, category):
    context = {}
    context['upcoming_events'] = functions.get_upcoming_events()
    qPage = models.Page.objects.all().filter(category=category)
    context['qPage'] = qPage
    context['page_title'] = page_titles[category]
    return render(request, 'pages/list.html', context)

@csrf_exempt
def upload_image(request):
    context = {}
    if request.method == 'POST':
        image = request.POST.get('image')
        if image:
            imageArr = image.split(',')
            i = 0
            while os.path.exists(UPLOADS_DIR + 'page_images/image_' + str(i) + '.png'):
                i += 1
            image_name = 'image_' + str(i) + '.png'     # placeholder
            image_path = '/static/uploads/page_images/' + image_name
            fh = open(UPLOADS_DIR + "page_images/" + image_name, "wb")
            fh.write(imageArr[1].decode('base64'))
            fh.close()
            return HttpResponse(json.dumps(image_path), content_type = "application/json")
    return HttpResponse(json.dumps('fail'), content_type = "application/json")
    


