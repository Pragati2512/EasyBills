from django.shortcuts import render, redirect, HttpResponseRedirect
#from django.http import HttpResponse
from . dtdalgo import detect
from . dtdalgo import entityextract
from django.core.files.storage import FileSystemStorage
from Profile.models import Profile,group
from . models import ProcessedData
from django.db.models import Q
from django.urls import reverse

def doctype(request):
    x = detect()
    return render(request, 'doctype.html', {'doctype': x})


def home(request):
    response = redirect('/upload/')
    return response

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        doctype, text = detect(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'doctype': doctype,
            'text': text
        })
    return render(request, 'upload.html')


def trial(request,grp_id):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        doctype, text = detect(filename)
        pro = Profile.objects.get(user=request.user)
        grp = group.objects.get(pk=grp_id)
        entityextract(filename,pro,grp)
        #invoice_id, order_id, customer_id, date_issue, amount_total, amount_due, sender_name, sender_address, sender_vat_id, recipient_name, recipient_address, all_items = entityextract(filename,pro,grp)
        return redirect("Profile:my-groups")
    return redirect("Profile:my-groups")


def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']
        if srch:
            match = ProcessedData.objects.filter(Q(recipient_name__icontains=srch) |
                                          Q(sender_name__icontains=srch) |
                                          Q(all_items__icontains=srch)  )
            if match:
                return render(request, 'search.html', {'sr': match})
            else:
                print(srch)
                #messages.error(request, 'No result found')
                return render(request, 'search.html', {'sr': match})
        else:
            return HttpResponseRedirect(reverse('Profile:my-groups'))

