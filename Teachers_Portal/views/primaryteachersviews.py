from django.shortcuts import render
from Student_Portal.models import *
from ..models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# from CBT.models import *
import json
from django.db.models import Q


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
    return render(request,'teachers/Primary_Result_computation.html',context)

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
            student_result_details, created = Student_Result_Data.objects.get_or_create(Student_name=student_result,Term=term,AcademicSession=session)
            student_result_object, created = PrimaryResult.objects.get_or_create(Subject=subjectobject, students_result_summary=student_result_details)
            studentResults.append({
                'Name': student_result_object.students_result_summary.Student_name.student_name,
                'Test': student_result_object.Test,
                'Exam': student_result_object.Exam,
                "published": student_result_object.published,
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
        studentResult.published = True
        studentResult.save()
    return JsonResponse('Results submitted Successfully', safe=False)


def primary_unsubmitallstudentresult_view(request):
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
        studentResult.published = False
        studentResult.save()
    return JsonResponse('Results unpublished Successfully', safe=False)


# ---------------------------------------------------------------------------------------------------------------------
# Primary School Annual Result View
# ---------------------------------------------------------------------------------------------------------------------
def annualresult_computation(request,Classname,id):
    teacher = Teacher.objects.get(id=id)
    academic_session= AcademicSession.objects.all()
    classobject = Class.objects.get(Class=Classname)
    subjectsforclass=Subjectallocation.objects.get(classname=classobject)
    subjects_taught_for_class = teacher.subjects_taught.filter(id__in=subjectsforclass.subjects.values_list('id', flat=True))
    context={
        'class':classobject,
        "academic_session":academic_session,
        "subjects_taught_for_class":subjects_taught_for_class
        } 
    return render(request,'teachers/Annual_Results.html',context)

def primary_annual_result_computation_view(request):
    data = json.loads(request.body)
    subject_name = data['studentsubject']
    class_name = data['studentclass']
    academic_session = data['selectedAcademicSession']
    
    class_object = Class.objects.get(Class=class_name)
    session = AcademicSession.objects.get(session=academic_session)
    subject_object = Subject.objects.get(subject_name=subject_name)
    students = Students_Pin_and_ID.objects.filter(student_class=class_object)
    terms = Term.objects.all()
    
    students_annuals = []
    for student in students:
        studentAnnual, created = AnnualStudent.objects.get_or_create(Student_name=student, academicsession=session)
        student_annual_details, created = AnnualResult.objects.get_or_create(Student_name=studentAnnual, Subject=subject_object)
        
        student_annual_details.Total = 0  # Ensure Total is initialized to zero
        termsobject = {}  # Reset for each student

        for term in terms:
            try:
                student_result_details, _ = Student_Result_Data.objects.get_or_create(
                    Student_name=student, Term=term, AcademicSession=session)
                student_result, _ = PrimaryResult.objects.get_or_create(
                    students_result_summary=student_result_details, Subject=subject_object)
                termsobject[term.term] = student_result.Total_100
            except Exception as e:
                print(f"Exception: {e}")
                continue
        try:
            students_annuals.append({
                "studentID": student.student_id,
                'Name': student.student_name,
                'terms': termsobject,
                'published': student_annual_details.published
            })
        except Exception as e:
            print(f"Exception: {e}")
            continue

    return JsonResponse(students_annuals, safe=False)


def publish_annual_results(request):
    data = json.loads(request.body)
    subject_name = data['classdata']['studentsubject']
    class_name = data['classdata']['studentclass']
    academic_session = data['classdata']['selectedAcademicSession']
    class_object = Class.objects.get(Class=class_name)
    session = AcademicSession.objects.get(session=academic_session)
    subject_object = Subject.objects.get(subject_name=subject_name)
    for result in data['data']:
        student = Students_Pin_and_ID.objects.get(student_id=result['studentID'], student_name=result['Name'], student_class=class_object)
        studentAnnual = AnnualStudent.objects.get(Student_name=student, academicsession=session)
        student_annual_details = AnnualResult.objects.get(Student_name=studentAnnual, Subject=subject_object)
        student_annual_details.FirstTermTotal = result["terms"]["1st Term"]
        student_annual_details.SecondTermTotal = result["terms"]["2nd Term"]
        student_annual_details.ThirdTermTotal = result["terms"]["3rd Term"]
        student_annual_details.Total = result['Total']
        student_annual_details.Average = result['Average']
        student_annual_details.Grade = result['Grade']
        student_annual_details.SubjectPosition = result['Position']
        student_annual_details.Remark = result['Remarks']
        student_annual_details.published = True
        student_annual_details.save()
    return JsonResponse('Results have been published', safe=False)


def unpublish_annual_results(request):
    data = json.loads(request.body)
    subject_name = data['classdata']['studentsubject']
    class_name = data['classdata']['studentclass']
    academic_session = data['classdata']['selectedAcademicSession']
    class_object = Class.objects.get(Class=class_name)
    session = AcademicSession.objects.get(session=academic_session)
    subject_object = Subject.objects.get(subject_name=subject_name)
    for studentdata in data['data']:
        student = Students_Pin_and_ID.objects.get(student_name=studentdata['Name'], student_class=class_object)
        studentAnnual = AnnualStudent.objects.get(Student_name=student, academicsession=session)
        student_annual_details = AnnualResult.objects.get(Student_name=studentAnnual, Subject=subject_object)
        student_annual_details.published = False
        student_annual_details.save()
    return JsonResponse('Results have been unpublished', safe=False)

