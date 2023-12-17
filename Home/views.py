from django.shortcuts import render
from .models import *
from Student_Portal.models import Students_Pin_and_ID
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

# Create your views here.
def home_view(request):
    managements=Management.objects.all().order_by('SN')
    topteacher = TopTeacher.objects.all().order_by('SN')
    photos=PhotoGallery.objects.all()[:6]
    faqs=FAQ.objects.all()
    events = UpcomingEvents.objects.all()
    parentsreview = ParentsReview.objects.all()
    context={
        "managements":managements,
        "Teachers":topteacher,
        "photos":photos,
        "parentsreviews":parentsreview,
        "events": events,
        "faqs":faqs
    }
    return render(request,'home.html',context)

def student_card_view(request):
    P = Paginator(Students_Pin_and_ID.objects.all(),21)
    page= request.GET.get('page')
    students = P.get_page(page)
    context = {
        "students":students
    }
    return render(request,'Activation.html',context)

def about_view(request):
    managements=Management.objects.all().order_by('SN')
    topteacher = TopTeacher.objects.all().order_by('SN')
    context={    
        "managements":managements,
        "Teachers":topteacher
    }
    return render(request,'About.html',context)

def photogallery_view(request):
    Pictures=PhotoGallery.objects.all().order_by('id')
    context={
        "Pictures":Pictures
    }
    return render(request,'Photogallery.html',context)

def submit_contact_form(request):
    data=json.loads(request.body)
    contactname=data['userformdata']['name']
    contactemail=data['userformdata']['email']
    contactmessage=data['userformdata']['message']
    contact_info=Contact.objects.create(
        name=contactname,
        email=contactemail,
        message=contactmessage
    )
    contact_info.save()

    return JsonResponse('submitted successfully',safe=False)

def submit_sub_form(request):
    data=json.loads(request.body)
    subemail=data['userdata']['email']
    sub_email=Subscription.objects.create(Email=subemail)
    sub_email.save()
    return JsonResponse('submitted successfully',safe=False)