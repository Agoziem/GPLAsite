from django.shortcuts import render
from .models import *
from Student_Portal.models import Students_Pin_and_ID
from django.core.paginator import Paginator

# Create your views here.
def home_view(request):
    managements=Management.objects.all().order_by('SN')[:9]
    topteacher = TopTeacher.objects.all().order_by('SN')[:9]
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