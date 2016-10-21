from __future__ import unicode_literals
import pretty

from django.db import models
from django.conf import settings
from django.utils.timezone import localtime

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Post(TimeStampedModel):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body        = models.TextField(max_length=1000)
    
    # POST: postId, uid, username, userImage, body, date, editable
    # COMMENTS: commentId, uid, username, userImage, body, date
    # IMAGES: array of image paths
    def objectify(self, currentUid):
        result = {}
        result['postId'] = self.id
        result['uid'] = self.user.id
        result['username'] = self.user.username
        if hasattr(self.user, 'profile'):
            result['userImage'] = '/static/' + self.user.profile.get_image()
        else:
            result['userImage'] = '/static/img/generic_user.png'
        result['body'] = self.body
        result['date'] = pretty.date( localtime( self.created ).replace(tzinfo=None) )
        if self.user.id == currentUid:
            result['editable'] = True
        else:
            result['editable'] = False
        # append comments
        result['comments'] = []
        qComment = PostComment.objects.all().filter(post=self)
        for oComment in qComment:
            comment = {
                'commentId' : oComment.id,
                'uid' : oComment.user.id,
                'username' : oComment.user.username,
                'userImage' : '/static/img/generic_user.png',
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
    
    def objectify(self, currentUid):
        response = {
            'postId' : self.post.id,
            'commentId' : self.id,
            'uid' : self.user.id,
            'username' : self.user.username,
            'userImage' : '/static/img/generic_user.png',
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

        

