from django.shortcuts import render
from .models import *
import base64
base64.encodestring = base64.encodebytes
base64.decodestring = base64.decodebytes
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse

# get students for each Class

def get_Students(request, Classname):
	classobject=Class.objects.get(Class=Classname)
	Students = Students_Pin_and_ID.objects.filter(student_class=classobject)
	Students_list = list(Students.values('id', 'student_name'))
	return JsonResponse(Students_list, safe=False)

# Result Portal View 
def Result_Portal_view(request):
	classes=Class.objects.all()
	Terms=Term.objects.all()
	academicsession= AcademicSession.objects.all()
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
		# Get the Student details, the c Students_Result_Details and the Results (Both Annual & Termly )
		try:
			resultTerm=Term.objects.get(term=term)
			resultSession= AcademicSession.objects.get(session=academic_session)
			student = Students_Pin_and_ID.objects.get(student_name=student_name,student_id=student_id,student_pin=Pin)
			if Student_Result_Data.objects.filter(Student_name=student,Term=resultTerm,AcademicSession=resultSession).exists():
				Student_Result_details=Student_Result_Data.objects.get(Student_name=student,Term=resultTerm,AcademicSession=resultSession)
				Student_Results=Result.objects.filter(students_result_summary=Student_Result_details)
				for result in Student_Results:
					labels.append(result.Subject)
					data.append(result.Total)
					
				if AnnualStudent.objects.filter(Student_name=student).exists():
					Annual_Result=True
					Annual_Student_Result_details=AnnualStudent.objects.get(Student_name=student,AcademicSession=resultSession)
					Annual_Student_Results=AnnualResult.objects.filter(students_result_data=Annual_Student_Result_details)
					PromotionVerdict=int(float(Annual_Student_Result_details.Average))
					context={
						"student_details":student,
						"Result_details":Student_Result_details,
						"Results":Student_Results,
						"labels":labels,
						"data":data,
						"AnnualStudent":Annual_Student_Result_details,
						'AnnualResult': Annual_Student_Results,
						"Annual_Result":Annual_Result,
						"PromotionVerdict":PromotionVerdict,
						}
					return render(request,"Result.html", context)
				else:
					Annual_Result=False	
					context={
						"Annual_Result":Annual_Result,
						"student_details":student,
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
				"academic_session":academicsession
			}
			messages.error(request, 'Check your Student id or the Pin and try again , make sure you are entering it Correctly')
			return render(request, "Result_Portal.html",context)
	
	context={
		"classes":classes,
		"Terms":Terms,
		"academic_session":academicsession
	}
	return render(request, "Result_Portal.html",context)
	

