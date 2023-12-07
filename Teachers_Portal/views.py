from django.shortcuts import render, redirect, get_object_or_404
from Student_Portal.models import *
from .models import *
from django.http import JsonResponse
from .forms import TeacherForm
from django.contrib.auth.decorators import login_required
# from CBT.models import *
import json
from django.db.models import Q


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
    return render(request,'editprofile.html',context)

# Secondary School Result Views
@login_required
def result_computation_view(request,Classname,id):
    teacher = Teacher.objects.get(id=id)
    Terms=Term.objects.all()
    academic_session= AcademicSession.objects.all()
    classobject = Class.objects.get(Class=Classname)
    subjectsforclass=Subjectallocation.objects.get(classname=classobject)
    subjects_taught_for_class = teacher.subjects_taught.filter(id__in=subjectsforclass.subjects.values_list('id', flat=True))
    context={
        'class':classobject,
        "Terms":Terms,
        "academic_session":academic_session,
        "subjects_taught_for_class":subjects_taught_for_class
        } 
    return render(request,'Secondary_Result_computation.html',context)

@login_required
def get_students_result_view(request):
    data=json.loads(request.body)
    studentResults = []
    try:
        classobject = Class.objects.get(Class=data['studentclass'])
        subjectobject = Subject.objects.get(subject_name=data['studentsubject'])
        term=Term.objects.get(term=data['selectedTerm'])
        session=AcademicSession.objects.get(session=data['selectedAcademicSession'])
        students = Students_Pin_and_ID.objects.filter(student_class=classobject)
        for studentresult in students:
            student_result_details,created = Student_Result_Data.objects.get_or_create(Student_name=studentresult,Term=term,AcademicSession=session)
            student_result_object, created = Result.objects.get_or_create(Subject=subjectobject, students_result_summary=student_result_details)
            
            studentResults.append({
                'Name': student_result_object.students_result_summary.Student_name.student_name,
                '1sttest': student_result_object.FirstTest,
                '1stAss': student_result_object.FirstAss,
                'Project': student_result_object.Project,
                'MidTermTest': student_result_object.MidTermTest,
                '2ndTest': student_result_object.SecondAss,
                '2ndAss': student_result_object.SecondTest,
                'Exam': student_result_object.Exam,
            })
        return JsonResponse(studentResults, safe=False)
    except:
        return JsonResponse(studentResults, safe=False)


@login_required
def update_student_result_view(request):
    data=json.loads(request.body)
    subject=data['classdata']['studentsubject']
    Classdata=data['classdata']['studentclass']
    student=data['formDataObject']['Name']
    classobject= Class.objects.get(Class=Classdata)
    term=Term.objects.get(term=data['classdata']['selectedTerm'])
    session=AcademicSession.objects.get(session=data['classdata']['selectedAcademicSession'])
    studentobject= Students_Pin_and_ID.objects.get(student_name=student,student_class=classobject)
    subjectobject = Subject.objects.get(subject_name=subject)
    student_result_details = Student_Result_Data.objects.get(Student_name=studentobject,Term=term,AcademicSession=session)
    studentResult = Result.objects.get(students_result_summary=student_result_details, Subject=subjectobject)
    studentResult.FirstTest  = data['formDataObject']['1sttest']
    studentResult.FirstAss  = data['formDataObject']['1stAss']
    studentResult.Project  = data['formDataObject']['Project']
    studentResult.MidTermTest  = data['formDataObject']['MidTermTest']
    studentResult.SecondAss = data['formDataObject']['2ndAss']
    studentResult.SecondTest = data['formDataObject']['2ndTest']
    studentResult.Exam = data['formDataObject']['Exam']
    studentResult.save()

    return JsonResponse('Result Updated Successfully', safe=False)
    

def submitallstudentresult_view(request):
    data=json.loads(request.body)
    subject=data['classdata']['studentsubject']
    Classdata=data['classdata']['studentclass']
    term=Term.objects.get(term=data['classdata']['selectedTerm'])
    session=AcademicSession.objects.get(session=data['classdata']['selectedAcademicSession'])
    for result in data['data']:
        classobject= Class.objects.get(Class=Classdata)
        subjectobject = Subject.objects.get(subject_name=subject)
        studentobject= Students_Pin_and_ID.objects.get(student_name=result['Name'],student_class=classobject)
        student_result_details = Student_Result_Data.objects.get(Student_name=studentobject,Term=term,AcademicSession=session)
        studentResult = Result.objects.get(students_result_summary=student_result_details, Subject=subjectobject)
        studentResult.FirstTest=result['1sttest']
        studentResult.FirstAss=result['1stAss']
        studentResult.Project=result['Project']
        studentResult.MidTermTest=result['MidTermTest']
        studentResult.SecondAss=result['2ndTest']
        studentResult.SecondTest=result['2ndAss']
        studentResult.CA=result['CA']
        studentResult.Exam=result['Exam']
        studentResult.Total=result['Total']
        studentResult.Grade=result['Grade']
        studentResult.SubjectPosition=result['Position']
        studentResult.Remark=result['Remarks']
        studentResult.save()
    return JsonResponse('Results submitted Successfully', safe=False)


# Primary School Result View
@login_required
def primary_result_computation_view(request,Classname,id):
    teacher = Teacher.objects.get(id=id)
    Terms=Term.objects.all()
    academic_session= AcademicSession.objects.all()
    classobject = Class.objects.get(Class=Classname)
    subjectsforclass=Subjectallocation.objects.get(classname=classobject)
    # subjects_taught_for_class = teacher.subjects_taught.filter(id__in=subjectsforclass.subjects.values_list('id', flat=True))
    context={
        'class':classobject,
        "Terms":Terms,
        "academic_session":academic_session,
        "subjects_taught_for_class":subjectsforclass
        } 
    return render(request,'Primary_Result_computation.html',context)

@login_required
def primary_get_students_result_view(request):
    data=json.loads(request.body)
    studentResults = []
    try:
        classobject = Class.objects.get(Class=data['studentclass'])
        subjectobject = Subject.objects.get(subject_name=data['studentsubject'])
        term=Term.objects.get(term=data['selectedTerm'])
        session=AcademicSession.objects.get(session=data['selectedAcademicSession'])
        studentsobjects = Students_Pin_and_ID.objects.filter(student_class=classobject)
        for student_result in studentsobjects:
            student_result_details,created = Student_Result_Data.objects.get_or_create(Student_name=student_result,Term=term,AcademicSession=session)
            student_result_object, created = PrimaryResult.objects.get_or_create(Subject=subjectobject, students_result_summary=student_result_details)
            studentResults.append({
                'Name': student_result_object.students_result_summary.Student_name.student_name,
                'Test': student_result_object.Test,
                'Exam': student_result_object.Exam,
            })
        return JsonResponse(studentResults, safe=False)
    except:
        return JsonResponse(studentResults, safe=False)

@login_required
def primary_update_student_result_view(request):
    data=json.loads(request.body)
    subject=data['classdata']['studentsubject']
    Classdata=data['classdata']['studentclass']
    student=data['formDataObject']['Name']
    classobject= Class.objects.get(Class=Classdata)
    term=Term.objects.get(term=data['classdata']['selectedTerm'])
    session=AcademicSession.objects.get(session=data['classdata']['selectedAcademicSession'])
    studentobject= Students_Pin_and_ID.objects.get(student_name=student,student_class=classobject)
    subjectobject = Subject.objects.get(subject_name=subject)
    student_result_details = Student_Result_Data.objects.get(Student_name=studentobject,Term=term,AcademicSession=session)
    studentResult = PrimaryResult.objects.get(students_result_summary=student_result_details, Subject=subjectobject)
    studentResult.Test  = data['formDataObject']['Test']
    studentResult.Exam = data['formDataObject']['Exam']
    studentResult.save()
    return JsonResponse('Result Updated Successfully', safe=False)
    

def primary_submitallstudentresult_view(request):
    data=json.loads(request.body)
    subject=data['classdata']['studentsubject']
    Classdata=data['classdata']['studentclass']
    term=Term.objects.get(term=data['classdata']['selectedTerm'])
    session=AcademicSession.objects.get(session=data['classdata']['selectedAcademicSession'])
    for result in data['data']:
        classobject= Class.objects.get(Class=Classdata)
        subjectobject = Subject.objects.get(subject_name=subject)
        studentobject= Students_Pin_and_ID.objects.get(student_name=result['Name'],student_class=classobject)
        student_result_details = Student_Result_Data.objects.get(Student_name=studentobject,Term=term,AcademicSession=session)
        studentResult = PrimaryResult.objects.get(students_result_summary=student_result_details, Subject=subjectobject)
        studentResult.Test=result['Test']
        studentResult.Exam=result['Exam']
        studentResult.Total_100=result['Total']
        studentResult.Grade=result['Grade']
        studentResult.SubjectPosition=result['Position']
        studentResult.Remark=result['Remarks']
        studentResult.save()
    return JsonResponse('Results submitted Successfully', safe=False)


# ////////////////////////////

# Form teachers View for CRUD Students Details
@login_required
def Students_view(request,Classname):
    classobject = Class.objects.get(Class=Classname)
    students = Students_Pin_and_ID.objects.filter(student_class=classobject)
    context={
        'class':classobject,
        "students":students
        } 
    return render(request,'students.html',context)

def createstudent_view(request):
    data=json.loads(request.body)
    student_name=data['studentname']
    student_sex=data['Student_sex']
    student_class=data['studentclass']
    classobject = Class.objects.get(Class=student_class)
    try:
        newStudent = Students_Pin_and_ID.objects.create(student_name=student_name,Sex=student_sex,student_class=classobject)
        newStudentResult = Student_Result_Data.objects.create(Student_name=newStudent)
        context={
            'student_ID': newStudent.id, 
            'student_id': newStudent.student_id, 
            'student_name':newStudent.student_name,
            'student_sex':newStudent.Sex,
            'message': f'{newStudent.student_name} record have been created Successfully'
        }
        return JsonResponse(context, safe=False)
    except:
        return JsonResponse({'error': 'something went wrong' }, safe=False)
    
def updatestudent_view(request):
    data=json.loads(request.body)
    student_id=data['studentID']
    student_name=data['studentname']
    student_sex=data['Student_sex']
    student_class=data['studentclass']
    classobject = Class.objects.get(Class=student_class)
    try:
        updateStudent = Students_Pin_and_ID.objects.get(id=student_id)
        updateStudent.student_name=student_name
        updateStudent.Sex= student_sex
        updateStudent.student_class=classobject
        updateStudent.save()
        context={
            'student_ID': updateStudent.id, 
            'student_id': updateStudent.student_id, 
            'student_name':updateStudent.student_name,
            'student_sex':updateStudent.Sex,
            'message': f'{updateStudent.student_name} record have been updated Successfully'
        }
        return JsonResponse(context, safe=False)
    except:
        return JsonResponse({'error': 'something went wrong' }, safe=False)

def DeleteStudents_view(request):
    studentidstodelete=json.loads(request.body)
    studentnamesdeleted=[]   
    try:
        for id in studentidstodelete:
            student = Students_Pin_and_ID.objects.get(id=id)
            studentnamesdeleted.append(student.student_name)
            student.delete()
        context={
            'message': f'{studentnamesdeleted} records have been deleted Successfully'
        }
        return JsonResponse(context, safe=False)
    except:
        return JsonResponse({'error': 'something went wrong' }, safe=False)


# Views for Publishing Students Result
@login_required
def PublishResults_view(request,Classname):
    Terms=Term.objects.all()
    academic_session= AcademicSession.objects.all()
    class_object = Class.objects.get(Class=Classname)
    subjects_allocation = Subjectallocation.objects.filter(classname=class_object).first()
    subject_code = []
    for subobject in subjects_allocation.subjects.all():
        subject_code.append(subobject.subject_code)
    context = {
        'subjects_allocation': subjects_allocation,
        "class": class_object,
        'sub_list':subject_code,
        "Terms":Terms,
        "academic_session":academic_session
        }
    return render(request, 'Publish_Result.html', context)

def getstudentsubjecttotals_view(request):
    data=json.loads(request.body)
    class_object = Class.objects.get(Class=data['studentclass'])
    term_object = Term.objects.get(term=data['selectedTerm'])
    session_object = AcademicSession.objects.get(session=data['selectedAcademicSession'])
    subjects_allocated = Subjectallocation.objects.filter(classname=class_object).first()
    students = Students_Pin_and_ID.objects.filter(student_class=class_object)
    final_list = []
    print(session_object,term_object)
    # get all the Students related to the Class
    for student in students:
        Resultdetails=Student_Result_Data.objects.filter(Student_name=student,Term=term_object,AcademicSession=session_object).first()
        student_dict = {
            'Name': student.student_name,
        }
        for subobject in subjects_allocated.subjects.all():
            try:
                if class_object.Class_section.section == 'Primary':
                    subresult = PrimaryResult.objects.get(students_result_summary=Resultdetails, Subject=subobject)
                    student_dict[subobject.subject_code] = subresult.Total_100
                else:
                    subresult = Result.objects.get(students_result_summary=Resultdetails, Subject=subobject)
                    student_dict[subobject.subject_code] = subresult.Total
            except:
                student_dict[subobject.subject_code] = "-"
        final_list.append(student_dict)
    return JsonResponse(final_list, safe=False)

def publishstudentresult_view(request):
    data=json.loads(request.body)
    termobject=data['classdata']['selectedTerm']
    Acadsessionobject=data['classdata']['selectedAcademicSession']
    Classdata=data['classdata']['studentclass']
    for studentdata in data['data']:
        classobject=Class.objects.get(Class=Classdata)
        resultterm = Term.objects.get(term=termobject)
        resultsession = AcademicSession.objects.get(session=Acadsessionobject)
        student = Students_Pin_and_ID.objects.get(student_name=studentdata['Name'],student_class=classobject)
        studentnumber=Students_Pin_and_ID.objects.filter(student_class=classobject).count()
        if Student_Result_Data.objects.filter(Student_name=student,Term=resultterm,AcademicSession=resultsession).exists():
            studentresult=Student_Result_Data.objects.get(Student_name=student,Term=resultterm,AcademicSession=resultsession)
            studentresult.TotalScore=studentdata['TOTAL']
            studentresult.Totalnumber= studentnumber
            studentresult.Average=studentdata['AVE']
            studentresult.Position=studentdata['POSITION']
            studentresult.Remark=studentdata['REMARK']
            studentresult.save()
        else:
            Student_Result_Data.objects.create(
            TotalScore=studentdata['TOTAL'],
            Average=studentdata['AVE'],
            Position=studentdata['POSITION'],
            Remark=studentdata['REMARK'],
            Student_name=student,
            Totalnumber= studentnumber,
            Term=resultterm,
            Academicsession=resultsession
            )
    return JsonResponse('Results have been Published and its now open to the Students', safe=False)


# for Class Attendance
@login_required
def attendance_view(request,Classname):
    classobject = Class.objects.all()
    context={
        'class':classobject
    }
    return render(request, 'attendance.html', context)

# Post Class Attendance
def post_attendance(request,classname):
    context={

    }
    return JsonResponse(context)






	
