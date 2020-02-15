from django.contrib import admin
from .models import tweet,follow,notification,comment

# Register your models here.
admin.site.register(tweet)
admin.site.register(follow)
admin.site.register(notification)
admin.site.register(comment)