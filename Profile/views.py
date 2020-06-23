from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .forms import RegistrationForm, UserForm , GroupForm
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, User , group , group_Member
from docdata.models import GroupDataLink ,RawData , ProcessedData
import pyotp
from twilio.rest import Client as TwilioClient
from decouple import config
import os
from twilio.http.http_client import TwilioHttpClient


proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config("TWILIO_AUTH_TOKEN")
twilio_phone = config("TWILIO_PHONE")
client = TwilioClient(account_sid, auth_token, http_client=proxy_client)



def home(request):
    return render(request, 'home/homepage2.html')


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

def register(request):
    form1 = UserForm()
    form2 = RegistrationForm()
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = RegistrationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            uss = form1.save()
            pro=form2.save(False)
            pro.user = uss
            pro.key = generate_key()
            form2.save(True)
            login(request, uss)
            return redirect("Profile:sms")
        message = 'ERROR !! Could not register. Please try again. '
        print("Error")
        context = {'message': message , 'form1': form1,'form2': form2 }
        return render(request,  'registration/registration_form2.html', context)
    return render(request, 'registration/registration_form2.html', {'form1': form1,'form2': form2 })


def login_request(request):
    message = ''
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                message = "Success: You are now logged in as {{username}}."
                return render(request, 'home/homepage2.html',{"message": message,})
            else:
                message = "Error: Invalid username or password."
        else:
            message = "Error: Invalid username or password."
    form = AuthenticationForm()
    context = {"form": form,
               "message": message, }
    return render(  request = request, template_name = "registration/login.html", context=context)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("Profile:home")


def send_sms_code(request, format=None):
    uss = request.user
    pro = Profile.objects.get(user=uss)
    time_otp = pyotp.TOTP(pro.key, interval=300)
    time_otp = time_otp.now()
    user_phone_number = pro.number
    client.messages.create(
        body="Your verification code is " + time_otp + ". -Pragati Tandon :)",
        from_=twilio_phone,
        to=user_phone_number
    )
    return redirect("Profile:verify-otp")


def verify_phone(request):
    if request.method == "POST":
        code = request.POST.get('otp')
        #code = int(sms_code)
        pro = Profile.objects.get(user=request.user)
        if pro.authenticate(code):
           pro.verified = True
           pro.save()
           message= "Phone number verified successfully"
           context = {"message": message,}
           return render(request, 'home/homepage2.html',context)
        else:
            message = "Error: The provided code did not match or has expired"
            context = {"message": message, }
            return render(request, 'home/homepage2.html', context)
    return render(request, 'Profile/verify_otp.html')


def Group_Create(request):
    if request.method == "POST":
        g_form = GroupForm(request.POST)
        if g_form.is_valid():
            grp = g_form.save(False)
            grp.admin = Profile.objects.get(user=request.user)
            g_form.save(True)
            gm = group_Member(group=grp, member=grp.admin)
            gm.save(True)
            return redirect('Profile:view-group', pk=grp.id)
    else:
        g_form = GroupForm()
        context = {"form": g_form, }
        return render(request, 'Profile/group_form.html', context)


def My_Groups(request):
    prsn = Profile.objects.get(user=request.user)
    grps = group_Member.objects.filter(member=prsn)
    grp_list = []
    for grp in grps:
         grp_list.append(grp)

    context = {"group_list": grp_list, }
    return render(request, 'Profile/my_groups.html', context)


def Group_View(request,pk):
    grp = group.objects.get(pk=pk)
    docs = GroupDataLink.objects.filter(group=grp)
    data = []
    for doc in docs:
        data.append(ProcessedData.objects.get(rawdata=doc.data))
    members = group_Member.objects.filter(group=grp)
    message = ''
    if request.method == "POST":
        phno = request.POST.get('phno')
        ppl = Profile.objects.filter(number=phno)
        if(ppl.count()==0):
            message = 'There is no such user with this phone number !!'
        for p in ppl:
            if(group_Member.objects.filter(group=grp, member=p).exists()):
                message = 'This user is already present in the group !!'
            else:
                gm = group_Member(group=grp, member=p)
                gm.save(True)
    context = {"group": grp, "logged_user_id" : request.user.id,
               "message": message,
               "members": members,
               "docs": data,
              }
    return render(request, 'Profile/view_group.html', context)

