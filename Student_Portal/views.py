from django.shortcuts import render
from .models import *
import base64
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse

# get students for each Class and academic session

def get_Students(request, Classname):
	classobject=Class.objects.get(Class=Classname)
	# Get academic session from request
	Session=request.GET.get('session')
	if Session:
		session = AcademicSession.objects.get(session=Session)
		enrollments = StudentEnrollment.objects.filter(student_class=classobject, academic_session=session)
	else:
		# Get students from the most recent enrollment for this class
		enrollments = StudentEnrollment.objects.filter(student_class=classobject).select_related('student')
	
	Students_list = [{'id': enrollment.student.pk, 'student_name': enrollment.student.student_name} 
	                 for enrollment in enrollments]
	return JsonResponse(Students_list, safe=False)

# Result Portal View 
def Result_Portal_view(request):
	classes=Class.objects.all()
	Terms=Term.objects.all()
	academic_sessions= AcademicSession.objects.all()
	if request.method == 'POST':
	# get the Student name from the request
		student_name=str(request.POST['student_name'])
		student_id=str(request.POST['student_id'])
		Pin=str(request.POST['student_pin'])
		term = request.POST['Term']
		academic_session = request.POST['AcademicSession']
		labels=[]
		data=[]
		Annual_Result=False
		# Get the Student details, the Students_Result_Details and the Results (Both Annual & Termly )
		try:
			resultTerm=Term.objects.get(term=term)
			resultSession= AcademicSession.objects.get(session=academic_session)
			studentClass=Class.objects.get(Class=request.POST['student_class'])
			
			# Get student and verify enrollment for this class in this session
			student = Students_Pin_and_ID.objects.get(student_name=student_name, student_id=student_id, student_pin=Pin)
			enrollment = StudentEnrollment.objects.filter(
				student=student, 
				student_class=studentClass, 
				academic_session=resultSession
			).first()
			
			if not enrollment:
				messages.error(request, 'Student is not enrolled in this class for the selected session')
				context={
					"classes":classes,
					"Terms":Terms,
					"academic_sessions":academic_sessions
				}
				return render(request, "Result_Portal.html", context)
			
			if Student_Result_Data.objects.filter(Student_name=student,Term=resultTerm,AcademicSession=resultSession,published=True).exists():
				Student_Result_details=Student_Result_Data.objects.filter(Student_name=student,Term=resultTerm,AcademicSession=resultSession,published=True).first()
				if studentClass.Class_section and studentClass.Class_section.section == 'Primary':
					Student_Results=PrimaryResult.objects.filter(students_result_summary=Student_Result_details,published=True)
					for result in Student_Results:
						labels.append(result.Subject.subject_name)
						data.append(result.Total_100)
				else:
					Student_Results=Result.objects.filter(students_result_summary=Student_Result_details,published=True)
					for result in Student_Results:
						labels.append(result.Subject.subject_name)
						data.append(result.Total)

				if AnnualStudent.objects.filter(Student_name=student,published=True, academicsession=resultSession).exists() and resultTerm.term == "3rd Term":
					Annual_Result=True
					Annual_Student_Result_details=AnnualStudent.objects.get(Student_name=student,academicsession=resultSession,published=True)
					Annual_Student_Results=AnnualResult.objects.filter(Student_name=Annual_Student_Result_details,published=True)
					context={
						"student_details":student,
						"enrollment": enrollment,
						"Result_details":Student_Result_details,
						"Results":Student_Results,
						"labels":labels,
						"data":data,
						"AnnualStudent":Annual_Student_Result_details,
						'AnnualResult': Annual_Student_Results,
						"Annual_Result":Annual_Result,
						}
					return render(request,"Result.html", context)
				else:
					Annual_Result=False	
					context={
						"Annual_Result":Annual_Result,
						"student_details":student,
						"enrollment": enrollment,
						"Result_details":Student_Result_details,
						"Results":Student_Results,
						"labels":labels,
						"data":data,
								}
					return render(request,"Result.html", context)
			else:
				return render(request,"404.html")

		except Students_Pin_and_ID.DoesNotExist:
			context={
				"classes":classes,
				"Terms":Terms,
				"academic_sessions":academic_sessions
			}
			messages.error(request, 'Check your Student id or the Pin and try again , make sure you are entering it Correctly')
			return render(request, "Result_Portal.html",context)
	
	context={
		"classes":classes,
		"Terms":Terms,
		"academic_sessions":academic_sessions
	}
	return render(request, "Result_Portal.html",context)
	

