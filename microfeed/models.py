from __future__ import unicode_literals

from django.db import models

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Post(TimeStampedModel):
    uid         = models.IntegerField()
    body        = models.TextField(max_length=1000)

    
class PostView(TimeStampedModel):
    uid         = models.IntegerField()
    body        = models.TextField(max_length=1000)
    username    = models.CharField(max_length=100)
    user_image  = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = "microfeed_post_view"
        
# CREATE VIEW microfeed_post_view AS
# SELECT P.id, P.uid, P.body, P.created, P.modified, U.name AS `username`, F.filename as `user_image`
# FROM (microfeed_post P INNER JOIN users U ON P.uid = U.uid)
#         LEFT OUTER JOIN file_managed F ON U.picture = F.fid
# ORDER BY P.created DESC;


class Comment(TimeStampedModel):
    post        = models.ForeignKey("Post")
    uid         = models.IntegerField()
    body        = models.TextField(max_length=1000)

    
class CommentView(TimeStampedModel):
    post        = models.ForeignKey("Post")
    uid         = models.IntegerField()
    body        = models.TextField(max_length=1000)
    username    = models.CharField(max_length=100)
    user_image  = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = "microfeed_comment_view"
        
# CREATE VIEW microfeed_comment_view AS
# SELECT C.id, C.uid, C.post_id, C.body, C.created, C.modified, U.name AS `username`, F.filename as `user_image`
# FROM (microfeed_comment C INNER JOIN users U ON C.uid = U.uid)
#         LEFT OUTER JOIN file_managed F ON U.picture = F.fid
# ORDER BY C.created DESC;

        

