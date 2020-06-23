from django.urls import path
from . import views

app_name = 'docdata'

urlpatterns = [
    path('trial/<int:grp_id>', views.trial, name='trial'),
    path('upload/', views.upload),
    path('doctype/', views.doctype),
    path('search/', views.search, name='bill-search'),

]
