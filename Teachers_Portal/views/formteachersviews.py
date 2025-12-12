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
    # Get the latest academic session or allow filtering
    latest_session = AcademicSession.objects.order_by('-session').first()
    enrollments = StudentEnrollment.objects.filter(student_class=classobject, academic_session=latest_session).select_related('student')
    students = [enrollment.student for enrollment in enrollments]
    context={
        'class':classobject,
        "students":students,
        "current_session": latest_session
        } 
    return render(request,'formteachers/students.html',context)

def createstudent_view(request):
    data=json.loads(request.body)
    student_name=data['studentname']
    student_sex=data['Student_sex']
    student_class=data['studentclass']
    classobject = Class.objects.get(Class=student_class)
    try:
        # Create student without class relationship
        newStudent = Students_Pin_and_ID.objects.create(student_name=student_name, Sex=student_sex)
        
        # Get or create the latest academic session
        latest_session = AcademicSession.objects.order_by('-session').first()
        if not latest_session:
            return JsonResponse({'error': 'No academic session found. Please create one first.' }, safe=False)
        
        # Create enrollment for the student
        StudentEnrollment.objects.create(
            student=newStudent,
            student_class=classobject,
            academic_session=latest_session
        )
        
        newStudentResult = Student_Result_Data.objects.create(Student_name=newStudent)
        context={
            'student_ID': newStudent.pk, 
            'student_id': newStudent.student_id, 
            'student_name':newStudent.student_name,
            'student_sex':newStudent.Sex,
            'message': f'{newStudent.student_name} record have been created Successfully'
        }
        return JsonResponse(context, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'something went wrong: {str(e)}' }, safe=False)
    
def updatestudent_view(request):
    data=json.loads(request.body)
    student_id=data['studentID']
    student_name=data['studentname']
    student_sex=data['Student_sex']
    student_class=data['studentclass']
    classobject = Class.objects.get(Class=student_class)
    try:
        updateStudent = Students_Pin_and_ID.objects.filter(id=student_id).order_by("id").first()
        if not updateStudent:
            return JsonResponse({'error': 'Student not found' }, safe=False)
        updateStudent.student_name=student_name
        updateStudent.Sex= student_sex
        updateStudent.save()
        
        # Update enrollment for current session
        latest_session = AcademicSession.objects.order_by('-session').first()
        if latest_session:
            enrollment, created = StudentEnrollment.objects.get_or_create(
                student=updateStudent,
                academic_session=latest_session,
                defaults={'student_class': classobject}
            )
            if not created:
                enrollment.student_class = classobject
                enrollment.save()
        
        context={
            'student_ID': updateStudent.pk, 
            'student_id': updateStudent.student_id, 
            'student_name':updateStudent.student_name,
            'student_sex':updateStudent.Sex,
            'message': f'{updateStudent.student_name} record have been updated Successfully'
        }
        return JsonResponse(context, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'something went wrong: {str(e)}' }, safe=False)

def DeleteStudents_view(request):
    studentidstodelete=json.loads(request.body)
    studentnamesdeleted=[]   
    try:
        for id in studentidstodelete:
            student = Students_Pin_and_ID.objects.filter(id=id).order_by("id").first()
            if not student:
                return JsonResponse({'error': f'Student with id {id} not found' }, safe=False)
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
    subjects_allocation = Subjectallocation.objects.filter(classname=class_object).order_by('-id').first()
    subject_code = []
    for subobject in subjects_allocation.subjects.all(): # type: ignore
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
    subjects_allocated = Subjectallocation.objects.filter(classname=class_object).order_by('-id').first()
    # Get students enrolled in this class for this session
    enrollments = StudentEnrollment.objects.filter(student_class=class_object, academic_session=session_object).select_related('student')
    students = [enrollment.student for enrollment in enrollments]
    final_list = []
    for student in students:
        Resultdetails=Student_Result_Data.objects.filter(Student_name=student,Term=term_object,AcademicSession=session_object).first()
        student_dict = {
            'Name': student.student_name,
            'subjects': []
        }
        for subobject in subjects_allocated.subjects.all(): # type: ignore
            subject = {}
            try:
                if class_object.Class_section.section == 'Primary': # type: ignore
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
            student_dict['published'] = Resultdetails.published if Resultdetails else False
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
        # Get student by name and verify enrollment
        student = Students_Pin_and_ID.objects.filter(student_name=studentdata['Name']).order_by("id").first()
        if not student:
            continue
        enrollment = StudentEnrollment.objects.filter(student=student, student_class=classobject, academic_session=resultsession).first()
        if not enrollment:
            continue
        studentnumber=StudentEnrollment.objects.filter(student_class=classobject, academic_session=resultsession).count()
        try:
            studentresult=Student_Result_Data.objects.get(Student_name=student,Term=resultterm,AcademicSession=resultsession)
            studentresult.TotalScore=studentdata['Total']
            studentresult.Totalnumber= str(studentnumber)
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
            student = Students_Pin_and_ID.objects.filter(student_name=student_data['Name']).order_by("id").first()
            if not student:
                continue
            # Verify enrollment
            enrollment = StudentEnrollment.objects.filter(student=student, student_class=class_object, academic_session=acad_session_object).first()
            if not enrollment:
                continue
            try:
                student_result = Student_Result_Data.objects.get(
                    Student_name=student,
                    Term=term_object,
                    AcademicSession=acad_session_object
                )
                student_result.published=False
                student_result.save()
            except ObjectDoesNotExist as e:
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
    subjects_allocation = Subjectallocation.objects.filter(classname=class_object).order_by('-id').first()
    subject_code = []
    for subobject in subjects_allocation.subjects.all(): # type: ignore
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
    # Get students enrolled in this class for this session
    enrollments = StudentEnrollment.objects.filter(student_class=classobject, academic_session=Acadsessionobject).select_related('student')
    students = [enrollment.student for enrollment in enrollments]
    subjects_allocated = Subjectallocation.objects.filter(classname=classobject).order_by('-id').first()
    final_list = []
    published = False
    for student in students:
        studentdict={
            'Name':student.student_name,
            "subjects":[]
        }
        for subobject in subjects_allocated.subjects.all(): # type: ignore
            subject = {}
            try:
                subject_object = Subject.objects.get(subject_code=subobject.subject_code)
                studentAnnual = AnnualStudent.objects.get(Student_name=student, academicsession=Acadsessionobject)
                subjectAnnual = AnnualResult.objects.get(Student_name=studentAnnual, Subject=subject_object)
                subject['subject_code'] = subobject.subject_code
                subject['subject_name'] = subobject.subject_name
                subject['Average'] = subjectAnnual.Average
                subject['published'] = subjectAnnual.published
                published = studentAnnual.published
            except:
                subject['subject_code'] = subobject.subject_code
                subject['subject_name'] = subobject.subject_name
                subject['Average'] = "-"
                subject['published'] = False
                published = False
            studentdict['subjects'].append(subject)
            studentdict['published'] = published
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
            # Get student and verify enrollment
            student = Students_Pin_and_ID.objects.filter(student_name=studentdata['Name']).order_by("id").first()
            if not student:
                continue
            enrollment = StudentEnrollment.objects.filter(student=student, student_class=classobject, academic_session=resultsession).first()
            if not enrollment:
                continue
            studentnumber=StudentEnrollment.objects.filter(student_class=classobject, academic_session=resultsession).count()
            try:
                studentresult=AnnualStudent.objects.get(Student_name=student,academicsession=resultsession)
                studentresult.TotalScore=studentdata['Total']
                studentresult.Totalnumber= str(studentnumber)
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
    # Get students enrolled in this class for this session
    enrollments = StudentEnrollment.objects.filter(student_class=classobject, academic_session=Acadsessionobject).select_related('student')
    students = [enrollment.student for enrollment in enrollments]
    for student in students:
        try:
            studentresult=AnnualStudent.objects.get(Student_name=student,academicsession=Acadsessionobject)
            studentresult.published = False
            studentresult.save()
        except:
            continue
    return JsonResponse({"type":"success","message":"Results have been Unpublished and its now closed to the Students"}, safe=False)









	
