from __future__ import unicode_literals
import pretty

from django.db import models
from django.conf import settings
from django.utils.timezone import localtime
from django.contrib import admin




class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
        
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
    
    title           = models.CharField(max_length=255)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teaser          = models.TextField(blank=True, null=True)
    body            = models.TextField()
    address         = models.CharField(max_length=500, blank=True, null=True)
    order           = models.IntegerField(default=0)
    category        = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=RESTAURANT)
    
    def __str__(self):
        return self.title
    
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
    title       = models.CharField(max_length=30, null=True, blank=True)
    url         = models.CharField(max_length=500)
    order       = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
 
        
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
