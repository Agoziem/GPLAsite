from django.shortcuts import render
from Student_Portal.models import *
from ..models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# from CBT.models import *
import json
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

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
    return render(request,'formteachers/students.html',context)

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


# ----------------------------------------------------
# Views for Publishing Students Result
# ----------------------------------------------------
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
    return render(request, 'formteachers/Publish_Result.html', context)

def getstudentsubjecttotals_view(request):
    data=json.loads(request.body)
    class_object = Class.objects.get(Class=data['studentclass'])
    term_object = Term.objects.get(term=data['selectedTerm'])
    session_object = AcademicSession.objects.get(session=data['selectedAcademicSession'])
    subjects_allocated = Subjectallocation.objects.filter(classname=class_object).first()
    students = Students_Pin_and_ID.objects.filter(student_class=class_object)
    final_list = []
    for student in students:
        Resultdetails=Student_Result_Data.objects.filter(Student_name=student,Term=term_object,AcademicSession=session_object).first()
        student_dict = {
            'Name': student.student_name,
            'subjects': []
        }
        for subobject in subjects_allocated.subjects.all():
            subject = {}
            try:
                if class_object.Class_section.section == 'Primary':
                    subresult = PrimaryResult.objects.get(students_result_summary=Resultdetails, Subject=subobject)
                    subject['subject_code'] = subobject.subject_code
                    subject['subject_name'] = subobject.subject_name
                    subject['Total'] = subresult.Total_100
                    subject['published'] = subresult.published
                else:
                    subresult = Result.objects.get(students_result_summary=Resultdetails, Subject=subobject)
                    subject['subject_code'] = subobject.subject_code
                    subject['subject_name'] = subobject.subject_name
                    subject['Total'] = subresult.Total
                    subject['published'] = subresult.published
            except:
                subject['subject_code'] = subobject.subject_code
                subject['subject_name'] = subobject.subject_name
                subject['Total'] = "-"
                subject['published'] = False
            student_dict['subjects'].append(subject)
            student_dict['published'] = Resultdetails.published
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
        try:
            studentresult=Student_Result_Data.objects.get(Student_name=student,Term=resultterm,AcademicSession=resultsession)
            studentresult.TotalScore=studentdata['Total']
            studentresult.Totalnumber= studentnumber
            studentresult.Average=studentdata['Ave']
            studentresult.Position=studentdata['Position']
            studentresult.Remark=studentdata['Remarks']
            studentresult.published=True
            studentresult.save()
        except Exception as e:
            print(str(e))
            continue
    return JsonResponse({
            "type": "success",
            "message": "Results have been Published and are now open to the Students"
            }, safe=False)

def unpublish_classresults_view(request):
    try:
        data = json.loads(request.body)
        term_object = Term.objects.get(term=data['classdata']['selectedTerm'])
        acad_session_object = AcademicSession.objects.get(session=data['classdata']['selectedAcademicSession'])
        class_object = Class.objects.get(Class=data['classdata']['studentclass'])
        for student_data in data['data']:
            student = Students_Pin_and_ID.objects.get(student_name=student_data['Name'],student_class=class_object)
            try:
                student_result = Student_Result_Data.objects.get(
                    Student_name=student,
                    Term=term_object,
                    AcademicSession=acad_session_object
                )
                student_result.published=False
                student_result.save()
            except ObjectDoesNotExist:
                print(str(e))
                continue
        return JsonResponse(
            {
            "type": "success",
            "message": "Results have been Unpublished and are now closed to the Students"
            }
        , safe=False)

    except Exception as e:
        print(str(e))
        return JsonResponse({
            "type": "error",
            "message": "An error occurred while Unpublishing Student Results" 
        }, safe=False)
    

# -----------------------------------------------------------------------------------
# Annual views for the Form teachers
# -----------------------------------------------------------------------------------
@login_required
def PublishAnnualResults_view(request,Classname):
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
        "academic_session":academic_session
        }
    return render(request, 'formteachers/Annual_Publish_Result.html', context)


def annual_class_computation_view(request):
    data=json.loads(request.body)
    classobject=Class.objects.get(Class=data['studentclass'])
    Acadsessionobject=AcademicSession.objects.get(session=data['selectedAcademicSession'])
    students = Students_Pin_and_ID.objects.filter(student_class=classobject)
    subjects_allocated = Subjectallocation.objects.filter(classname=classobject).first()
    final_list = []
    for student in students:
        studentdict={
            'Name':student.student_name,
            "subjects":[]
        }
        for subobject in subjects_allocated.subjects.all():
            subject = {}
            try:
                subject_object = Subject.objects.get(subject_code=subobject.subject_code)
                studentAnnual = AnnualStudent.objects.get(Student_name=student, academicsession=Acadsessionobject)
                subjectAnnual = AnnualResult.objects.get(Student_name=studentAnnual, Subject=subject_object)
                subject['subject_code'] = subobject.subject_code
                subject['subject_name'] = subobject.subject_name
                subject['Average'] = subjectAnnual.Average
                subject['published'] = subjectAnnual.published
            except:
                subject['subject_code'] = subobject.subject_code
                subject['subject_name'] = subobject.subject_name
                subject['Average'] = "-"
                subject['published'] = False
            studentdict['subjects'].append(subject)
            studentdict['published'] = studentAnnual.published
        final_list.append(studentdict)
    return JsonResponse(final_list, safe=False)


# 
def publish_annualstudentresult_view(request):
    try:
        data=json.loads(request.body)
        Acadsessionobject=data['classdata']['selectedAcademicSession']
        Classdata=data['classdata']['studentclass']
        for studentdata in data['data']:
            classobject=Class.objects.get(Class=Classdata)
            resultsession = AcademicSession.objects.get(session=Acadsessionobject)
            student = Students_Pin_and_ID.objects.get(student_name=studentdata['Name'],student_class=classobject)
            studentnumber=Students_Pin_and_ID.objects.filter(student_class=classobject).count()
            try:
                studentresult=AnnualStudent.objects.get(Student_name=student,academicsession=resultsession)
                studentresult.TotalScore=studentdata['Total']
                studentresult.Totalnumber= studentnumber
                studentresult.Average=studentdata['Average']
                studentresult.Position=studentdata['Position']
                studentresult.Remark=studentdata['Remarks']
                studentresult.Verdict = studentdata['Verdict']
                studentresult.published = True
                studentresult.save()
            except Exception as e:
                print(str(e))
                continue
        return JsonResponse({
            "type": "success",
            "message": "Annual Results have been published and are now opened to the Students"
            }, safe=False)
    except:
        return JsonResponse({"type":"danger","message":"something went wrong, try again later" }, safe=False)
    

def unpublish_annual_classresults_view(request):
    data=json.loads(request.body)
    classobject=Class.objects.get(Class=data['classdata']['studentclass'])
    Acadsessionobject=AcademicSession.objects.get(session=data['classdata']['selectedAcademicSession'])
    students = Students_Pin_and_ID.objects.filter(student_class=classobject)
    for student in students:
        try:
            studentresult=AnnualStudent.objects.get(Student_name=student,academicsession=Acadsessionobject)
            studentresult.published = False
            studentresult.save()
        except:
            continue
    return JsonResponse({"type":"success","message":"Results have been Unpublished and its now closed to the Students"}, safe=False)









	
