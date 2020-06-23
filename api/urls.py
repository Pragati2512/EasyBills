from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users' , views.UsersList)
router.register(r'profile' , views.ProfileList)

urlpatterns = [
    path('', views.List, name='list'),

    path('v1/', include(router.urls) ),
    path('send_sms_code/<int:p_id>',views.send_sms_code),
    path('verify_phone/<int:p_id>/<int:sms_code>',views.verify_phone),


    #path('users/', views.UsersList.as_view() , name='users-list'),
    #path('profile/', views.ProfileList.as_view(), name='profile-list')
    path('raw_data/', views.RawDataDisplay.as_view(), name='raw-data'),
    path('bill_data/', views.GroupDataLinkDisplay.as_view(), name='bill-data'),
    path('processed_data/', views.ProcessedDataDisplay.as_view(), name='processed-data'),

    ]

