from django.contrib import admin
from . models import RawData, ProcessedData, BillItem, GroupDataLink

admin.site.register(RawData)
admin.site.register(ProcessedData)
admin.site.register(GroupDataLink)
admin.site.register(BillItem)
