from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
import datetime
# Create your models here.


class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/')


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("account:profile",kwargs={'username':self.user.username})

    # @property
    def in_followings(self):
        print(request.user)
        myfollowings=request.user.followings.all()
        user_list=[]
        for following in myfollowings:
            user_list.append(following.myuser)
            print(following.myuser)
        print(user_list)
        if self.user in user_list:
            return True
        else:
            return False
        

class user_lastseen(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    last_seen = models.DateTimeField(default=datetime.datetime.now())