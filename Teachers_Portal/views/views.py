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
        role = request.POST.get("Role")
        class_formed = request.POST.get("classFormed")
        if form.is_valid():
            # Update the Role
            teacher = form.save(commit=False)
            teacher.Role = role

            # Only assign classFormed if Role is 'Form-teacher'
            if role == "ClassTeacher":
                if class_formed:
                    teacher.classFormed_id = class_formed
            else:
                teacher.classFormed = None  # Reset if Role is not Form-teacher
            teacher.save()
            form.save_m2m()
            return redirect('Teachers_Portal:Teachers_dashboard')
    
    context={
        'teacher': teacher,
        'classes':classes,
        'subjects':subjects,
        'form':form
    }
    return render(request,'teachers/editprofile.html',context)









	
