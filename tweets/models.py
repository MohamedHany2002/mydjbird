from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect,reverse
import datetime
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.


class tweet(models.Model):
    text= models.CharField(max_length=250)
    created=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='tweets')
    slug=models.SlugField(null=True)
    likes=models.ManyToManyField(User,related_name='liked_tweets')
    dislikes=models.ManyToManyField(User,related_name='disliked_tweets')


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('single_tweet',kwargs={'id':self.id})


def slug_tweet(sender,**kwargs):
    if not kwargs['instance'].slug:
        slug_term=kwargs['instance'].text[:7]+"-"+kwargs['instance'].user.username
        kwargs['instance'].slug=slugify(slug_term)

pre_save.connect(slug_tweet,sender=tweet)
    

class comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    text=models.TextField(null=True)
    created=models.DateTimeField(auto_now_add=True)
    associated_tweet=models.ForeignKey(tweet,on_delete=models.CASCADE,null=True,related_name='comments')
    # user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)


class follow(models.Model):
    myuser=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='followers')
    anotheruser=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='followings')

    def __str__(self):
        return str(self.anotheruser)+"follows"+str(self.myuser)


class notification(models.Model):
    created=models.DateTimeField(auto_now_add=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='notified')
    users=models.ManyToManyField(User,related_name='related_notifs')
    url=models.URLField(null=True)
    










