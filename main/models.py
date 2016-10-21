from django.db import models
# from django.conf import settings

from django.contrib.auth.models import User
from django.contrib import admin




# User Model:  (from django.contrib.auth.models import User)
# *username - 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
# first_name
# last_name
# email
# *password
# groups
# user_permissions
# is_staff
# is_active
# is_superuser
# last_login (auto)
# date_joined (auto)
# ---
# get_username()
# is_authenticated()
# get_full_name()
# get_short_name()
# set_password(pw)
# check_password(pw)
# email_user(subject, message, from_email)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=30)
    
    def get_image(self):
        if self.image_name:
            return 'uploads/user_images/image_' + str(self.user.id) + '.png'
        else:
            return 'img/generic_user.png'
        
class ProfileAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Profile, ProfileAdmin)
        

