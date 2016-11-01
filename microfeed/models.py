from __future__ import unicode_literals
import pretty
import re

from django.db import models
from django.conf import settings
from django.utils.timezone import localtime

def replace_url_to_link(value):
    # Replace url to link
    urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="\1" target="_blank">\1</a>', value)
    # Replace email to mailto
    urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="mailto:\1">\1</a>', value)
    return value


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Post(TimeStampedModel):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body        = models.TextField(max_length=3000, blank=True, null=True)
    
    # POST: postId, uid, username, userImage, body, date, editable
    # COMMENTS: commentId, uid, username, userImage, body, date
    # IMAGES: array of image paths
    

    
    def get_formatted_body(self):
        value = self.body.replace('\n', '<br />')
        value = value.replace(' www.', ' http://www.')
        value = replace_url_to_link(value)
        return value
    
    def objectify(self, currentUid):
        result = {}
        result['postId'] = self.id
        result['uid'] = self.user.id
        result['username'] = self.user.username
        if hasattr(self.user, 'profile'):
            result['userImage'] = '/static/' + self.user.profile.get_image()
        else:
            result['userImage'] = '/static/img/generic_user.png'
        result['formatted_body'] = self.get_formatted_body()
        result['body'] = self.body
        result['date'] = pretty.date( localtime( self.created ).replace(tzinfo=None) )
        if self.user.id == currentUid:
            result['editable'] = True
        else:
            result['editable'] = False
        # extra info for events
        if hasattr(self, 'eventpost'):
            result['post_type'] = 'event'
            result['title'] = self.eventpost.title
            result['times'] = []
            for oTime in self.eventpost.eventposttime_set.all():
                temp = {}
                temp['startDate'] = oTime.start_date.strftime('%b %-d, %Y')
                temp['startTime'] = oTime.start_time.strftime('%I:%M%p').lstrip('0').lower()
                temp['endTime'] = oTime.end_time.strftime('%I:%M%p').lstrip('0').lower()
                result['times'].append(temp)
            result['editLink'] = '/microfeed/posts/view/' + str(self.id)
        else:
            result['post_type'] = 'standard'
        # append comments
        result['comments'] = []
        qComment = PostComment.objects.all().filter(post=self)
        for oComment in qComment:
            comment = {
                'commentId' : oComment.id,
                'uid' : oComment.user.id,
                'username' : oComment.user.username,
                'userImage' : '/static/img/generic_user.png',
                'formatted_body' : oComment.get_formatted_body(),
                'body' : oComment.body,
                'date' : pretty.date( localtime( oComment.created ).replace(tzinfo=None) ),
            }
            if hasattr(oComment.user, 'profile'):
                comment['userImage'] = '/static/' + oComment.user.profile.get_image()
            if oComment.user.id == currentUid:
                comment['editable'] = True
            else:
                comment['editable'] = False
            result['comments'].append(comment)
        result['images'] = []
        qPostImage = PostImage.objects.all().filter(post=self)
        for oPostImage in qPostImage:
            result['images'].append('/static/uploads/post_images/' + oPostImage.image_name)
        return result
        
    class Meta:
        ordering = ['-created']
        
class EventPost(TimeStampedModel):
    post        = models.OneToOneField("Post", on_delete=models.CASCADE, primary_key=True)
    title       = models.CharField(max_length=255)
    #start_date  = models.DateField()
    #start_time  = models.TimeField()
    #end_time    = models.TimeField(blank=True, null=True)
    
class EventPostTime(TimeStampedModel):
    event_post  = models.ForeignKey("EventPost", on_delete=models.CASCADE)
    start_date  = models.DateField()
    start_time  = models.TimeField()
    end_time    = models.TimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['start_date', 'start_time']
    
        
    
    
class PostImage(TimeStampedModel):
    post        = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_name  = models.CharField(max_length=30)
    order       = models.IntegerField()
    
    class Meta:
        ordering = ['order']
    
class PostComment(TimeStampedModel):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post        = models.ForeignKey("Post", on_delete=models.CASCADE)
    body        = models.TextField(max_length=1000)
    
    def get_formatted_body(self):
        value = self.body.replace('\n', '<br />')
        value = value.replace(' www.', ' http://www.')
        value = replace_url_to_link(value)
        return value
    
    def objectify(self, currentUid):
        response = {
            'postId' : self.post.id,
            'commentId' : self.id,
            'uid' : self.user.id,
            'username' : self.user.username,
            'userImage' : '/static/img/generic_user.png',
            'formatted_body' : self.get_formatted_body(),
            'body' : self.body,
            'date' : pretty.date( localtime( self.created ).replace(tzinfo=None) ),
        }
        if hasattr(self.user, 'profile'):
            response['userImage'] = '/static/' + self.user.profile.get_image()
        if self.user.id == currentUid:
            response['editable'] = True
        else:
            response['editable'] = False
        return response
    
    class Meta:
        ordering = ['created']


    
#class PostView(TimeStampedModel):
#    uid         = models.IntegerField()
#    body        = models.TextField(max_length=1000)
#    username    = models.CharField(max_length=100)
#    user_image  = models.CharField(max_length=255)
#    
#    class Meta:
#        managed = False
#        db_table = "microfeed_post_view"
        
# CREATE VIEW microfeed_post_view AS
# SELECT P.id, P.uid, P.body, P.created, P.modified, U.name AS `username`, F.filename as `user_image`
# FROM (microfeed_post P INNER JOIN users U ON P.uid = U.uid)
#         LEFT OUTER JOIN file_managed F ON U.picture = F.fid
# ORDER BY P.created DESC;



    
#class CommentView(TimeStampedModel):
#    post        = models.ForeignKey("Post", on_delete=models.DO_NOTHING)
#    uid         = models.IntegerField()
#    body        = models.TextField(max_length=1000)
#    username    = models.CharField(max_length=100)
#    user_image  = models.CharField(max_length=255)
#    
#    class Meta:
#        managed = False
#        db_table = "microfeed_comment_view"
        
# CREATE VIEW microfeed_comment_view AS
# SELECT C.id, C.uid, C.post_id, C.body, C.created, C.modified, U.name AS `username`, F.filename as `user_image`
# FROM (microfeed_comment C INNER JOIN users U ON C.uid = U.uid)
#         LEFT OUTER JOIN file_managed F ON U.picture = F.fid
# ORDER BY C.created;

        

