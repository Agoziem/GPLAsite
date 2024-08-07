from django.shortcuts import render, redirect
from Student_Portal.models import *
from ..models import *
from ..forms import TeacherForm
from django.contrib.auth.decorators import login_required


# Teachers Dashbord View
@login_required
def Teachers_dashboard_view(request):
    context={

    }
    return render(request,'Teachers_dashboard.html',context)

# Teachers profile View
@login_required
def profile_view(request,id):
    teacher = Teacher.objects.get(id=id)
    classes=Class.objects.all()
    subjects=Subject.objects.all()
    form = TeacherForm(instance=teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save() 
            return redirect('Teachers_Portal:Teachers_dashboard')
    
    context={
        'teacher': teacher,
        'classes':classes,
        'subjects':subjects,
        'form':form
    }
    return render(request,'teachers/editprofile.html',context)









	
