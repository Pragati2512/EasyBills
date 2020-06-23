from django.contrib import admin
from .models import Profile, group, group_Member

admin.site.register(Profile)
admin.site.register(group)
admin.site.register(group_Member)