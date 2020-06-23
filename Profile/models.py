from django.db import models
import pyotp
from django.contrib.auth.models import User
from enum import Enum
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=17, blank=True)
    location = models.CharField(max_length=30, blank=True , default="Blank")
    key = models.CharField(max_length=100, unique=True, blank=True)
    enable_authenticator = models.BooleanField(default=False)  # We can use this to enable 2fa for users
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def authenticate(self, otp):
        try:
            provided_otp = int(otp)
        except:
            return False
        t = pyotp.TOTP(self.key, interval=300)
        return t.verify(provided_otp)



class groupType(Enum):
    Family = "Family"
    Friends = "Friends"
    Business = "Business"
    Society = "Society"


class adm(Enum):
    Admin = "Admin only"
    Everyone = "Everyone"


class group(models.Model):
    name = models.CharField(max_length=30, blank=True)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE )
    created_on = models.DateField(default=datetime.date.today)
    type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in groupType],
                                   default=groupType.Family)
    adm_settings = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in adm],
                                   default=adm.Everyone)

    def __str__(self):
        return self.name


class group_Member(models.Model):
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    joined_on = models.DateField("Date", default=datetime.date.today)

    def __str__(self):
        return self.group.name + " " + self.member.user.username
