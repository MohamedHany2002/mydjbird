
from django.urls import path,include
from . import views
app_name='account'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/<str:username>',views.user_profile,name='profile'),
    path('search_user/<str:keyword>',views.search_user,name='search_user'),
    path('editprofile/',views.edit_profile,name='editprofile'),

]
