from django.shortcuts import render,HttpResponseRedirect,reverse,get_object_or_404
from .forms import user_form,profile_form,login_form,editprofileform,edituserform
from django.contrib.auth.models import User
from .models import profile,user_lastseen
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from tweets.models import follow
# Create your views here.

def register(request):
    if request.method=='POST':  
        userform=user_form(request.POST)
        profileform=profile_form(request.POST)
        if userform.is_valid() and profileform.is_valid():
            username=userform.cleaned_data.get('username')
            first_name=userform.cleaned_data.get('first_name')
            last_name=userform.cleaned_data.get('last_name')
            email=userform.cleaned_data.get('email')
            password=userform.cleaned_data.get('password')
            myuser=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            myprofile=profile.objects.create(user=myuser)
            image=request.FILES.get('image')
            myprofile.image=image
            myprofile.save()
            lastseen_object=user_lastseen()
            lastseen_object.user=myuser
            lastseen_object.save()
            login(request,myuser)
            return HttpResponseRedirect(reverse("tweets")) 

        else:
            return render(request,"account/signup.html",{'userform':userform})
    else:
        userform=user_form()
        profileform=profile_form()
        return render(request,'account/signup.html',{'userform':user_form,'profileform':profileform})

def user_login(request):
    if request.method=='POST':
        loginform=login_form()
        # if loginform.is_valid():
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        print(user)
        if user is not None:
            lastseen_object=get_object_or_404(user_lastseen,user__username=username)
            lastseen_object.last_seen=user.last_login
            # lastseen_object.previous_last_seen=datetime.datetime.now()
            lastseen_object.save()
            login(request,user)
            print("loggedin")
            return HttpResponseRedirect(reverse("tweets"))
        else:
            print("not loggedin ")
            error="user doesn't exist"
            return render(request,"account/login.html",{'loginform':loginform,'error':error})

    else:
        loginform=login_form()
        return render(request,"account/login.html",{'loginform':loginform}) 

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("account:login"))

def user_profile(request,username):
    logged_user=request.user
    if logged_user.related_notifs.all().exists():   
        user_notifs=logged_user.related_notifs.all().order_by('-created')[:4]
    else:
        user_notifs=[]
    logged_user=request.user
    flag=False
    user_flag=False
    myuser=get_object_or_404(User,username=username)
    user_followers=myuser.followers.all()
    user_list=[]
    for follower in user_followers:
        user_list.append(follower.anotheruser)
    if logged_user in user_list:
        flag=True
    if request.user == myuser:
        user_flag=True
    return render(request,"account/profile.html",{'myuser':myuser,'flag':flag,'user_flag':user_flag,'notifications':user_notifs})


def search_user(request,keyword):
    # keyword=request.GET.get('keyword')
    myusers=User.objects.filter(Q(username__icontains=keyword)|Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))
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
    
    return render(request,"account/search_user.html",{'myusers':myusers,'dict':mydict})


def edit_profile(request):
    if request.method=='POST':
        userform=edituserform(request.POST or None,instance=request.user)
        profileform=editprofileform(request.POST or None,instance=request.user.profile,files=request.FILES)
        if userform.is_valid() and profileform.is_valid():
            myuserform=userform.save(commit=False)
            myuserform.set_password(userform.cleaned_data['password'])
            myuserform.save()
            profileform.save()
            user=User.objects.get(id=myuserform.id)
            login(request,user)
            return HttpResponseRedirect(reverse("account:profile",kwargs={'username':user.username}))
        else:
            print("lol")
            return render(request,"account/editprofile.html",{'userform':userform})
    else:
        
        userform=edituserform(instance=request.user)
        profileform=editprofileform()
        return render(request,"account/editprofile.html",{'profileform':profileform,"userform":userform})

# def edit_profile(request):
#     if request.method=='POST':
#         userform=edituserform(request.POST,instance=request.user)
#         profileform=editprofileform(request.POST)
#         if userform.is_valid() and profileform.is_valid():
#             myuser=User.objects.get(username=request.user.username)
#             myprofile=profile.objects.get(user=request.user)
#             myuser.username=request.POST['username']
#             myuser.first_name=request.POST['first_name']
#             myuser.last_name=request.POST['last_name']
#             myuser.email=request.POST['email']
#             myuser.password=request.POST['password']
#             myuser.save()
#             myprofile.user=myuser
#             myprofile.image=request.FILES['image']
#             myprofile.save()
#             return HttpResponseRedirect(reverse("account:profile",kwargs={'username':request.user.username}))
#         else:
#             return render(request,"account/editprofile.html",{'userform':userform}) 
#     else:
#         profileform=editprofileform()
#         userform=edituserform()
#         return render(request,"account/editprofile.html",{'profileform':profileform,"userform":userform})
