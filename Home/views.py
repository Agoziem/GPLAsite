from django.shortcuts import render
from .models import *
from Student_Portal.models import Students_Pin_and_ID, StudentEnrollment, AcademicSession
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
    # Get all academic sessions for the dropdown
    academic_sessions = AcademicSession.objects.all().order_by('-session')
    
    # Get selected session from query params or use the latest
    selected_session_id = request.GET.get('session')
    if selected_session_id:
        selected_session = AcademicSession.objects.get(id=selected_session_id)
    else:
        selected_session = academic_sessions.first()
    
    # Get students enrolled in the selected session
    if selected_session:
        enrollments = StudentEnrollment.objects.filter(
            academic_session=selected_session
        ).select_related('student', 'student_class').order_by('student__student_name')
        
        # Create a list of student data with their enrollment info
        students_data = [{
            'student': enrollment.student,
            'student_class': enrollment.student_class,
            'enrollment': enrollment
        } for enrollment in enrollments]
        
        # Paginate the results
        P = Paginator(students_data, 21)
        page = request.GET.get('page')
        students = P.get_page(page)
    else:
        students = []
    
    context = {
        "students": students,
        "academic_sessions": academic_sessions,
        "selected_session": selected_session
    }
    return render(request, 'Activation.html', context)

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