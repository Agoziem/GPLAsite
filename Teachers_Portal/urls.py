from django.urls import path
from .views import *

app_name = 'Teachers_Portal'
urlpatterns = [
	path('',Teachers_dashboard_view , name='Teachers_dashboard'),
	path('<int:id>/profile/', profile_view , name='profile'),

	# urls for Form-Teachers Publishing Student Result
	path('<str:Classname>/PublishResults/',PublishResults_view , name='PublishResults'),   
	path('getstudentsubjecttotals/',getstudentsubjecttotals_view , name='getstudentsubjecttotals'),   
	path('publishstudentresult/',publishstudentresult_view , name='publishstudentresult'),
    
	# CRUD for Students
	path('<str:Classname>/Students/',Students_view , name='Students'),   
	path('newStudent/', createstudent_view , name='createstudent'),   
	path('updateStudent/', updatestudent_view , name='updatestudent'),   
	path('DeleteStudents/', DeleteStudents_view , name='DeleteStudents'),

	# Attendance  
	path('<str:Classname>/attendance',attendance_view, name='mark_attendance'),
    path('<str:classname>/post_attendance',post_attendance , name='post_attendance'),
    
	# CRUD for Teachers adding and updating Student Results
	path('<str:Classname>/<int:id>/result_computation/',result_computation_view , name='result_computation'),
	path('getstudentresults/',get_students_result_view , name='getstudentresults'),   
	path('updatestudentresults/',update_student_result_view , name='updatestudentresults'),   
	path('submitallstudentresult/',submitallstudentresult_view , name='submitallstudentresult'),

	# CRUD for Primary School Teachers adding and updating Student Results
	path('<str:Classname>/<int:id>/primary_result_computation/',primary_result_computation_view , name='primary_result_computation'),
    path('primarygetstudentresults/',primary_get_students_result_view , name='primarygetstudentresults'),   
	path('primaryupdatestudentresults/',primary_update_student_result_view , name='primaryupdatestudentresults'),   
	path('primarysubmitallstudentresult/',primary_submitallstudentresult_view , name='primarysubmitallstudentresult'),
]