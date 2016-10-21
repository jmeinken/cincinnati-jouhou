from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from feed.functions import validate_form_with_inlines



from . import models
from . import forms


def home(request):
    return HttpResponse("hello world")





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
            return HttpResponse('thanks')
    context['form'] = form
    context['children'] = children
    return render(request, 'pages/new_page.html', context)


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
            return HttpResponse('thanks')
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
    oPage = models.Page.objects.all().get(pk=page_id)
    context['oPage'] = oPage
    return render(request, 'pages/page.html', context)

def list(request, category):
    context = {}
    qPage = models.Page.objects.all().filter(category=category)
    context['qPage'] = qPage
    return render(request, 'pages/list.html', context)


