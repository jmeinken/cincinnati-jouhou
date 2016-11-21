from __future__ import unicode_literals
import pretty

from django.db import models
from django.conf import settings
from django.utils.timezone import localtime
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from field_trans.helpers import get_translation





class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
        
class ActivePageManager(models.Manager):
    def get_queryset(self):
        return super(ActivePageManager, self).get_queryset().filter(visible=True)
        
class Page(TimeStampedModel):
    RESTAURANT = 'restaurant'
    LOCAL_DESTINATION = 'local_destination'
    REGIONAL_DESTINATION = 'regional_destination'
    HOUSING = 'housing'
    SHOPPING = 'shopping'
    MEDICAL = 'medical'
    TRANSPORTATION = 'transportation'
    EDUCATION = 'education'
    CATEGORY_CHOICES = (
        (RESTAURANT, 'restaurant'),
        (LOCAL_DESTINATION, 'local_destination'),
        (REGIONAL_DESTINATION, 'regional_destination'),
        (HOUSING, 'housing'),
        (SHOPPING, 'shopping'),
        (MEDICAL, 'medical'),
        (TRANSPORTATION, 'transportation'),
        (EDUCATION, 'education'),
    )
    
    title           = models.CharField(max_length=255, verbose_name=_('title'),)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teaser          = models.TextField(blank=True, null=True, verbose_name=_('teaser'),)
    body            = models.TextField(blank=True, null=True, verbose_name=_('body'),)
    address         = models.CharField(max_length=500, blank=True, null=True, verbose_name=_('address'),)
    order           = models.IntegerField(default=0, verbose_name=_('order'),)
    category        = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=RESTAURANT, verbose_name=_('category'),)
    visible         = models.BooleanField(default=True)
    
    objects = models.Manager() # The default manager.
    visible_obj = ActivePageManager() # The Dahl-specific manager.
    
    def __str__(self):
        return self.title
    
    def has_translation(self):
        title = get_translation('page', 'title', self.id)
        body = get_translation('page', 'body', self.id)
        teaser = get_translation('page', 'teaser', self.id)
        if title or body or teaser:
            return True
        return False
    
    def trans_title(self):
        translation = get_translation('page', 'title', self.id)
        if translation:
            return translation
        else:
            return self.title
        
    def trans_body(self):
        translation = get_translation('page', 'body', self.id)
        if translation:
            return translation
        else:
            return self.body
        
    def trans_teaser(self):
        translation = get_translation('page', 'teaser', self.id)
        if translation:
            return translation
        else:
            return self.teaser
        
    def trans_only_title(self):
        translation = get_translation('page', 'title', self.id)
        if translation:
            return translation
        else:
            return ''
        
    def trans_only_body(self):
        translation = get_translation('page', 'body', self.id)
        if translation:
            return translation
        else:
            return ''
        
    def trans_only_teaser(self):
        translation = get_translation('page', 'teaser', self.id)
        if translation:
            return translation
        else:
            return ''
    
    class Meta:
        ordering = ['order', '-id']
        
        
class PageImage(TimeStampedModel):
    page        = models.ForeignKey("Page", on_delete=models.CASCADE)
    image       = models.ImageField(upload_to='page_images/', max_length=100)
    order       = models.IntegerField(default=0)
    
    def get_image_path(self):
        return self.image.url
    
    class Meta:
        ordering = ['order', 'id']
        
class PageLink(TimeStampedModel):
    page        = models.ForeignKey("Page", on_delete=models.CASCADE)
    title       = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('title'),)
    url         = models.CharField(max_length=500, verbose_name=_('url'),)
    order       = models.IntegerField(default=0, verbose_name=_('order'),)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = _('Page Link')
        verbose_name_plural = _('Page Links')
 
        
class PageComment(TimeStampedModel):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    page        = models.ForeignKey("Page", on_delete=models.CASCADE)
    body        = models.TextField(max_length=1000)
    
    def objectify(self, currentUid):
        response = {
            'postId' : self.page.id,
            'commentId' : self.id,
            'uid' : self.user.id,
            'username' : self.user.username,
            'userImage' : 'path/image.png',
            'body' : self.body,
            'date' : pretty.date( localtime( self.created ).replace(tzinfo=None) ),
        }
        if self.user.id == currentUid:
            response['editable'] = True
        else:
            response['editable'] = False
        return response
    
    class Meta:
        ordering = ['created']
        
### ADMIN #####################################################################



class PageImageAdmin(admin.TabularInline):    # can also use TabularInline
    model = PageImage
    extra = 3
    
class PageLinkAdmin(admin.TabularInline):    # can also use TabularInline
    model = PageLink
    extra = 3
    
class PageAdmin(admin.ModelAdmin):
    inlines = [PageImageAdmin, PageLinkAdmin]
    
admin.site.register(Page, PageAdmin)
