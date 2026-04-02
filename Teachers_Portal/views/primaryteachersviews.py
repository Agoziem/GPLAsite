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
    subjectsforclass=Subjectallocation.objects.filter(classname=classobject).order_by('-id').first()
    if subjectsforclass:
        subjects_taught_for_class = teacher.subjects_taught.filter(id__in=subjectsforclass.subjects.values_list('id', flat=True))
    else:
        subjects_taught_for_class = teacher.subjects_taught.none()
    print(subjects_taught_for_class)
    context={
        'class':classobject,
        "Terms":Terms,
        "academic_session":academic_session,
        "subjects_taught_for_class":subjects_taught_for_class
        } 
    return render(request,'teachers/Primary_Result_computation.html',context)

@login_required
def primary_get_students_result_view(request):
    data=json.loads(request.body)
    studentResults = []
    try:
        classobject = Class.objects.get(Class=data['studentclass'])
        subjectsforclass = Subjectallocation.objects.filter(classname=classobject).order_by('-id').first()
        if not subjectsforclass:
            return JsonResponse({'error': 'No subject allocation found for this class'}, safe=False)
        subjectobject = subjectsforclass.subjects.filter(subject_name=data['studentsubject']).first()
        if not subjectobject:
            return JsonResponse({'error': 'Subject not found in allocation for this class'}, safe=False)
        term=Term.objects.get(term=data['selectedTerm'])
        session=AcademicSession.objects.get(session=data['selectedAcademicSession'])
        # Get students enrolled in this class for this session
        enrollments = StudentEnrollment.objects.filter(student_class=classobject, academic_session=session).select_related('student')
        studentsobjects = [enrollment.student for enrollment in enrollments]
        for student_result in studentsobjects:
            try:
                student_result_details, created = Student_Result_Data.objects.get_or_create(Student_name=student_result,Term=term,AcademicSession=session)
                student_result_object, created = PrimaryResult.objects.get_or_create(Subject=subjectobject, students_result_summary=student_result_details)
                studentResults.append({
                    'id': student_result_object.students_result_summary.Student_name.pk, # type: ignore
                    'Name': student_result_object.students_result_summary.Student_name.student_name, # type: ignore
                    'Test': student_result_object.Test,
                    'Exam': student_result_object.Exam,
                    "published": student_result_object.published,
                })
            except Exception as e:
                print(f"Error processing student {student_result}: {e}")
                continue
        return JsonResponse(studentResults, safe=False)
    except Exception as e:
        print(f"primary_get_students_result_view error: {e}")
        return JsonResponse({'error': str(e)}, safe=False)

@login_required
def primary_update_student_result_view(request):
    data=json.loads(request.body)
    subject=data['classdata']['studentsubject']
    Classdata=data['classdata']['studentclass']
    classobject= Class.objects.get(Class=Classdata)
    term=Term.objects.get(term=data['classdata']['selectedTerm'])
    session=AcademicSession.objects.get(session=data['classdata']['selectedAcademicSession'])
    # Get student by pk and verify enrollment
    studentobject= Students_Pin_and_ID.objects.filter(pk=data['formDataObject']['id']).first()
    if not studentobject:
        return JsonResponse('Student not found', safe=False)
    enrollment = StudentEnrollment.objects.filter(student=studentobject, student_class=classobject, academic_session=session).first()
    if not enrollment:
        return JsonResponse('Student not enrolled in this class for this session', safe=False)
    subjectsforclass = Subjectallocation.objects.filter(classname=classobject).order_by('-id').first()
    subjectobject = subjectsforclass.subjects.filter(subject_name=subject).first() if subjectsforclass else None
    if not subjectobject:
        return JsonResponse('Subject not found for this class', safe=False)
    studentResult.Exam = data['formDataObject']['Exam']
    studentResult.save()
    return JsonResponse('Result Updated Successfully', safe=False)
    

def primary_submitallstudentresult_view(request):
    data=json.loads(request.body)
    subject=data['classdata']['studentsubject']
    Classdata=data['classdata']['studentclass']
    term=Term.objects.get(term=data['classdata']['selectedTerm'])
    session=AcademicSession.objects.get(session=data['classdata']['selectedAcademicSession'])
    classobject= Class.objects.get(Class=Classdata)
    subjectsforclass = Subjectallocation.objects.filter(classname=classobject).order_by('-id').first()
    subjectobject = subjectsforclass.subjects.filter(subject_name=subject).first() if subjectsforclass else None
    if not subjectobject:
        return JsonResponse('Subject not found for this class', safe=False)
    for result in data['data']:
        # Get student by pk and verify enrollment
        studentobject= Students_Pin_and_ID.objects.filter(pk=result['id']).first()
        if not studentobject:
            continue
        enrollment = StudentEnrollment.objects.filter(student=studentobject, student_class=classobject, academic_session=session).first()
        if not enrollment:
            continue
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
    classobject= Class.objects.get(Class=Classdata)
    subjectsforclass = Subjectallocation.objects.filter(classname=classobject).order_by('-id').first()
    subjectobject = subjectsforclass.subjects.filter(subject_name=subject).first() if subjectsforclass else None
    if not subjectobject:
        return JsonResponse('Subject not found for this class', safe=False)
    for result in data['data']:
        # Get student by pk and verify enrollment
        studentobject= Students_Pin_and_ID.objects.filter(pk=result['id']).first()
        if not studentobject:
            continue
        enrollment = StudentEnrollment.objects.filter(student=studentobject, student_class=classobject, academic_session=session).first()
        if not enrollment:
            continue
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
    subjectsforclass=Subjectallocation.objects.filter(classname=classobject).order_by('-id').first()
    subjects_taught_for_class = teacher.subjects_taught.filter(id__in=subjectsforclass.subjects.values_list('id', flat=True)) # type: ignore
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
    # Get students enrolled in this class for this session
    enrollments = StudentEnrollment.objects.filter(student_class=class_object, academic_session=session).select_related('student')
    students = [enrollment.student for enrollment in enrollments]
    terms = Term.objects.all()
    
    students_annuals = []
    for student in students:
        studentAnnual, created = AnnualStudent.objects.get_or_create(Student_name=student, academicsession=session)
        student_annual_details, created = AnnualResult.objects.get_or_create(Student_name=studentAnnual, Subject=subject_object)

        student_annual_details.Total = str(0)  # Ensure Total is initialized to zero
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
                "id": student.pk,
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
        # Get student and verify enrollment
        student = Students_Pin_and_ID.objects.filter(pk=result['id']).first()
        if not student:
            continue
        enrollment = StudentEnrollment.objects.filter(student=student, student_class=class_object, academic_session=session).first()
        if not enrollment:
            continue
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
        # Get student by pk and verify enrollment
        student = Students_Pin_and_ID.objects.filter(pk=studentdata['id']).first()
        if not student:
            continue
        enrollment = StudentEnrollment.objects.filter(student=student, student_class=class_object, academic_session=session).first()
        if not enrollment:
            continue
        studentAnnual = AnnualStudent.objects.get(Student_name=student, academicsession=session)
        student_annual_details = AnnualResult.objects.get(Student_name=studentAnnual, Subject=subject_object)
        student_annual_details.published = False
        student_annual_details.save()
    return JsonResponse('Results have been unpublished', safe=False)

