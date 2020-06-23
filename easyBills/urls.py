from django.contrib import admin
from django.urls import path , include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('Profile.urls', namespace="Profile")),
    path('api/', include('api.urls', namespace="api")),
    path('', include('docdata.urls', namespace="docdata")),

]
