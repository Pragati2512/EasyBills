from django.db import models
from django.utils import timezone
from Profile.models import Profile , group
timezone.localtime(timezone.now())
import json_field


class RawData(models.Model):
    source_file = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now)
    time_created = models.TimeField(default=timezone.now)
    user = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    device_transfer = json_field.JSONField(lazy=False, null=True)
    json_data = json_field.JSONField(lazy=False)

    def __str__(self):
        return self.source_file


class GroupDataLink(models.Model):
    group = models.ForeignKey(group, blank=True, null=True, on_delete=models.CASCADE)
    data = models.ForeignKey(RawData, blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.group.name


class BillItem(models.Model):
    rawdata = models.ForeignKey(RawData, blank=True, null=True, on_delete=models.CASCADE)
    item_name = models.CharField(null=True, max_length=50)
    item_quantity = models.CharField(null=True, max_length=10)
    item_total_amount = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.item_name


class ProcessedData(models.Model):
    rawdata = models.ForeignKey(RawData, blank=True, null=True, on_delete=models.CASCADE)
    invoice_id = models.CharField(null=True, max_length=30)
    order_id = models.CharField(null=True, max_length=20)
    customer_id = models.CharField(null=True, max_length=15)
    date_issue = models.CharField(null=True, max_length=12)
    amount_total = models.CharField(null=True, max_length=10)
    amount_due = models.CharField(null=True, max_length=10)
    sender_name = models.CharField(null=True, max_length=30)
    sender_address = models.CharField(null=True, max_length=200)
    sender_vat_id = models.CharField(null=True, max_length=30)
    recipient_name = models.CharField(null=True, max_length=30)
    recipient_address = models.CharField(null=True, max_length=200)
    all_items = models.CharField(null=True, max_length=3000)

    def __str__(self):
        return self.rawdata.source_file