from django.shortcuts import render,HttpResponseRedirect,reverse,get_object_or_404
from django.shortcuts import redirect
from .models import tweet,notification,follow,comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from account.models import user_lastseen
import datetime
from django.template.loader import render_to_string
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

# Create your views here.

@login_required
def tweets(request):
    user=request.user
    user_notifs=user.related_notifs.all().order_by('-created')[:5]
    myfollowings=user.followings.all()
    list_followings=[]  
    for following in myfollowings:
        list_followings.append(following.myuser)
    mytweet=tweet.objects.filter(user__in=list_followings).order_by('-created')[:1]
    tweets=tweet.objects.filter(user__in=list_followings)
    if mytweet.exists():
        last_created_tweet=mytweet.first().created
    else:
        last_created_tweet=datetime.datetime.now()
    # print('mm',mytweet.first().created)
    print(user.user_lastseen.last_seen)
    print(user.last_login)
    # print(user.user_lastseen.last_seen>mytweet.first().created)
    qs_list=[]
    users_dict={}
    users_active_list=[]
    myusers_active_list=[]

 
###
    for anyuser in User.objects.all():
        if anyuser not in list_followings:
            users_active_list.append(anyuser)
    for anyuser in users_active_list:
        count=anyuser.tweets.all().count()
        users_dict[anyuser]=count
    

    for anyuser in users_dict:
        print(users_dict[anyuser],anyuser)
        
    mysortedusers=sorted(users_dict.items(),key=lambda x:x[1])
    all_sorted_users=list(reversed(mysortedusers))
    print(all_sorted_users,'hahah')
    for active in all_sorted_users:
        myusers_active_list.append(active[0])
    print(myusers_active_list,"nono")

    ###
    if mytweet.exists():
        if user.user_lastseen.last_seen>last_created_tweet:
            mydict={}
            active_list=[]
            for following in list_followings:
                print("this",following)
                count=following.tweets.all().count()
                mydict[following]=count
            for key,value in mydict.items():
                print("ok",key,mydict[key])
            sorted_users=sorted(mydict.items(),key=lambda x:x[1])
            most_active_users=list(reversed(sorted_users))
            for active in most_active_users:
                active_list.append(active[0])
            for each_user in active_list:
                qs=tweets.filter(user=each_user)
                qs_list.append(qs.order_by('-created'))
            return render(request,"tweets/mytweets.html",{'notifications':user_notifs,'qs_list':qs_list,"actives":myusers_active_list[:6]})
        else:
            print("get out there")
            mytweets=tweet.objects.filter(user__in=list_followings).order_by('-created')[:50]
            return render(request,"tweets/tweets.html",{'tweets':mytweets,'notifications':user_notifs,"actives":myusers_active_list[:6]})
    else:
        new=True
        return render(request,"tweets/tweets.html",{'new':new,"actives":myusers_active_list[:6]})
    



def delete_tweet(request,id):
    mytweet=get_object_or_404(tweet,id=id)
    mytweet.delete()
    return HttpResponseRedirect(reverse("account:profile",kwargs={'username':mytweet.user.username}))



def edit_tweet(request,id):
    text=request.POST['text']
    mytweet=tweet.objects.get(id=id)
    user=mytweet.user
    mytweet.delete()
    tweet.objects.create(text=text,user=user)
    return HttpResponseRedirect(reverse("account:profile",kwargs={'username':mytweet.user.username}))


def post_tweet(request):
    text=request.POST['text']
    user=request.user
    error=''
    if len(text)>250:
        error='max length exceeded'
        return render(request,"tweets/tweets.html",{'error':error})
    mytweet=tweet.objects.create(text=text,user=user)
    mytweet.save()
    user_followers=user.followers.all()
    url=mytweet.get_absolute_url()

    mynotify=notification.objects.create(user=user,url=url)
    for follower in user_followers:
        mynotify.users.add(follower.anotheruser)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def single_tweet(request,id):   
    mytweet=tweet.objects.get(id=id)
    return render(request,"tweets/single_tweet.html",{'mytweet':mytweet})


# def tweet_comment(request):
#     print("finaly motherfucker")
#     text=request.POST['text']
#     print(text)
#     tweet_id=request.POST['myid']
#     print("this nice id",tweet_id)
#     # tweet_id=request.POST['tweet_id']
#     # print("okkk",tweet_id)
#     mytweet=tweet.objects.get(id=tweet_id)
    
#     mycomment=comment.objects.create(text=text,user=request.user)
#     mycomment.associated_tweet=mytweet
#     mycomment.save()
#     comments=mytweet.comments.all()
#     # context={'tweet':mytweet,'comment':mycomment}
#     # return render(request,"tweets",context)
#     # comments=mytweet.comments.all
#     context={'comments':comments,'tweet':mytweet}
#     if request.is_ajax(): 
#         html=render_to_string('tweets/comment.html',context,request=request)
#         return JsonResponse({'form':html})
#     # return HttpResponseRedirect(reverse("single_tweet",args=[mytweet.id]))
#     return redirect(request.META.get('HTTP_REFERER', '/'))





def tweet_comment(request):
    text=request.POST['text']
    tweet_id=request.POST['tweet_id']
    mytweet=tweet.objects.get(id=tweet_id)
    # print(mytweet.text)
    mycomment=comment.objects.create(text=text,user=request.user)
    # mycomment.user=request.user
    # associated_tweet.comments.add()

    mycomment.associated_tweet=mytweet
    mycomment.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
    # return HttpResponseRedirect(reverse("single_tweet",args=[mytweet.id]))



def tweet_like(request,id):
    mytweet = get_object_or_404(tweet,id=id)
    user=request.user
    if user not in mytweet.likes.all():
        if user in mytweet.dislikes.all():
            mytweet.dislikes.remove(user)
        mytweet.likes.add(user)
    print(mytweet.likes)
    print(mytweet.dislikes)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def tweet_dislike(request,id):
    mytweet = get_object_or_404(tweet,id=id)
    user=request.user
    if user not in mytweet.dislikes.all():
        if user in mytweet.likes.all():
            mytweet.likes.remove(user)
        mytweet.dislikes.add(user)
    print(mytweet.likes)
    print(mytweet.dislikes)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def follow_user(request):
    logged_user=request.user
    username=request.POST['username']

    myuser=get_object_or_404(User,username=username)
    follow_object=follow.objects.create(myuser=myuser,anotheruser=logged_user)
  
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def unfollow_user(request):
    username=request.POST['username']
    myuser=get_object_or_404(User,username=username)
    following_user=request.user
    myfollow_object=myuser.followers.filter(anotheruser=following_user)
    myfollow_object.first().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # return HttpResponseRedirect(reverse('account:profile',kwargs={'username':username}))



def search_update(request,keyword):
    # keyword=request.GET.get('keyword')
    tweets=tweet.objects.filter(Q(text__icontains=keyword)|Q(user__username__icontains=keyword)).order_by('-created')
    return render(request,"tweets/search_update.html",{'tweets':tweets})


def user_followers(request,id):
    print("hey")
    myuser=get_object_or_404(User,id=id)
    all_followers=myuser.followers.all()
    users_list=[]
    for each_follower in all_followers:
        users_list.append(each_follower.anotheruser)
    print("all",all_followers)
    return render(request,"account/followers.html",{'follwers':users_list})



def user_followings(request,id):
    myuser=get_object_or_404(User,id=id)
    all=myuser.followings.all()
    users_list=[]
    for each_follower in all:
        users_list.append(each_follower.myuser)
    return render(request,"account/followers.html",{'follwers':users_list})


def search(request):
    keyword=request.GET.get('keyword')
    tweets=tweet.objects.filter(Q(text__icontains=keyword)|Q(user__username__icontains=keyword)).order_by('-created')[:3]
    myusers=User.objects.filter(Q(username__icontains=keyword)|Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))[:3]
    if len(myusers)==0:
        user_flag=True
    else:
        user_flag=False
    if len(tweets)==0:
        update_flag=True
    else:
        update_flag=False
    all_followings=request.user.followings.all()
    mylist=[]
    mydict={}
    for following in all_followings:
        mylist.append(following.myuser)
    for user in myusers:
        if user in mylist:
            mydict[user]=True
        else:
            mydict[user]=False

    return render(request,"tweets/search.html",{'tweets':tweets,'myusers':myusers,'keyword':keyword,'dict':mydict,'user_flag':user_flag,'update_flag':update_flag})

def notifications(request):
    user=request.user
    user_notifs=user.related_notifs.all().order_by('-created')
    return render(request,"tweets/notifications.html",{'notifications':user_notifs})