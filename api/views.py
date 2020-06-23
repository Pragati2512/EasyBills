from django.shortcuts import render
from rest_framework import permissions,viewsets, status , generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProfileSerializer, UserSerializer
from .serializers import RawDataSerializer, ProcessedDataSerializer, GroupDataLinkSerializer
from Profile.models import Profile, User
from docdata.models import RawData, ProcessedData, GroupDataLink
import pyotp

from django.shortcuts import HttpResponse
from twilio.rest import Client as TwilioClient
from decouple import config
import os
from twilio.http.http_client import TwilioHttpClient


proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config("TWILIO_AUTH_TOKEN")
twilio_phone = config("TWILIO_PHONE")
client = TwilioClient(account_sid, auth_token, http_client=proxy_client)


def List(request):
    return render(request, 'api/api_list.html')


class ProfileList(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


def generate_key():
        key = pyotp.random_base32()
        if is_unique(key):
            return key
        generate_key()

def is_unique(key):
        try:
            Profile.objects.get(key=key)
        except Profile.DoesNotExist:
            return True
        return False

def create_key(p_id):
        instance = Profile.objects.get(id=p_id)
        if not instance.key:
            instance.key = generate_key()

        def perform_create(self, serializer):
            serializer.save()


def send_sms_code(request,p_id, format=None):
    pro = Profile.objects.get(id=p_id)
    create_key(p_id)
    time_otp = pyotp.TOTP(pro.key, interval=300)
    time_otp = time_otp.now()
    user_phone_number = pro.number
    client.messages.create(
                     body="Your verification code is " + time_otp + ". -Pragati Tandon :)",
                     from_=twilio_phone,
                     to=user_phone_number
                 )
    #return Response(dict(detail = "SMS sent successfully !!! "),status=201)
    return HttpResponse("Sending OTP to  " + user_phone_number  +  "  ...Mobile check karo")


def verify_phone(request,p_id,sms_code, format=None):
    code = int(sms_code)
    pro = Profile.objects.get(id=p_id)
    if pro.authenticate(code):
        pro.verified=True
        pro.save()
        return HttpResponse("Phone number verified successfully")
        #return Response(dict(detail = "Phone number verified successfully"),status=201)
    #return Response(dict(detail='The provided code did not match or has expired'),status=200)
    return HttpResponse("The provided code did not match or has expired")

'''
class ProfileList(APIView):
    def get(self,request):
        pers = Profile.objects.all()
        serial=ProfileSerializer(pers,many=True)
        return Response(serial.data)

    def post(self):
        pass


class UsersList(viewsets.ModelViewSet()):
        queryset = User.objects.all()
        serializer_class = UserSerializer

class UsersList(APIView):
    def get(self,request):
        pers = User.objects.all()
        serial=UserSerializer(pers,many=True)
        return Response(serial.data)

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''

class UsersList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()



class RawDataDisplay(APIView):
    def get(selfself, request):
        RawData1 = RawData.objects.all()
        serializer = RawDataSerializer(RawData1, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ProcessedDataDisplay(APIView):
    def get(selfself, request):
        ProcessedData1 = ProcessedData.objects.all()
        serializer = ProcessedDataSerializer(ProcessedData1, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class GroupDataLinkDisplay(APIView):
    def get(selfself, request):
        data = GroupDataLink.objects.all()
        serializer = GroupDataLinkSerializer(data, many=True)
        return Response(serializer.data)

    def post(self):
        pass

