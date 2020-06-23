from django.urls import path
from . import views

app_name = 'Profile'

urlpatterns = [
    path('', views.home , name='home'),
    path("login/", views.login_request, name='login'),
    path('register/', views.register, name='register'),
    path("logout/", views.logout_request, name='logout'),
    #path('users/api', views.UsersList.as_view(), name='users-list-api'),
    #path('profile/api', views.ProfileList.as_view(), name='profile-list-api'),
    path('group/new', views.Group_Create, name='create-group'),
    path('mygroups/', views.My_Groups, name='my-groups'),
    path('<int:pk>/group', views.Group_View, name='view-group'),

    path('send_sms_code/',views.send_sms_code, name='sms'),
    path('verify_phone/',views.verify_phone, name='verify-otp'),
    #path('group/add/', views.AddMember, name='add-member'),
    #path('<int:pk>/mygroups/', views.Group_View, name='view-group'),
]
