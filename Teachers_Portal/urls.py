from django.urls import path
from .views.views import *
from .views.adminviews import *
from .views.formteachersviews import *
from .views.primaryteachersviews import *
from .views.secondaryteachersviews import *


app_name = 'Teachers_Portal'
urlpatterns = [
	path('',Teachers_dashboard_view , name='Teachers_dashboard'),
	path('<int:id>/profile/', profile_view , name='profile'),

	# urls for Form-Teachers Publishing Student Result
	path('<str:Classname>/PublishResults/',PublishResults_view , name='PublishResults'),   
	path('getstudentsubjecttotals/',getstudentsubjecttotals_view , name='getstudentsubjecttotals'),   
	path('publishstudentresult/',publishstudentresult_view , name='publishstudentresult'),
    path('unpublishclassresult/',unpublish_classresults_view , name='unpublishstudentresult'),
    path('<str:Classname>/AnnualResults/',PublishAnnualResults_view , name='AnnualResults'), 
    path('annualclassresultcomputation/',annual_class_computation_view , name='annualclassresultcomputation'),
    path('publishannualclassresult/',publish_annualstudentresult_view , name='publishannualresult'),
    path('unpublishannualclassresult/',unpublish_annual_classresults_view , name='unpublishannualresult'),
    
	# CRUD for Students
	path('<str:Classname>/Students/',Students_view , name='Students'),   
	path('newStudent/', createstudent_view , name='createstudent'),   
	path('updateStudent/', updatestudent_view , name='updatestudent'),   
	path('DeleteStudents/', DeleteStudents_view , name='DeleteStudents'),

	# CRUD for Secondary Teachers adding and updating Student Results
	path('<str:Classname>/<int:id>/result_computation/',result_computation_view , name='result_computation'),
	path('getstudentresults/',get_students_result_view , name='getstudentresults'),   
	path('updatestudentresults/',update_student_result_view , name='updatestudentresults'),   
	path('submitallstudentresult/',submitallstudentresult_view , name='submitallstudentresult'),
	path('unsubmitallstudentresult/',unsubmitallstudentresult_view , name='unsubmitallstudentresult'),

	# CRUD for Primary School Teachers adding and updating Student Results
	path('<str:Classname>/<int:id>/primary_result_computation/',primary_result_computation_view , name='primary_result_computation'),
    path('primarygetstudentresults/',primary_get_students_result_view , name='primarygetstudentresults'),   
	path('primaryupdatestudentresults/',primary_update_student_result_view , name='primaryupdatestudentresults'),   
	path('primarysubmitallstudentresult/',primary_submitallstudentresult_view , name='primarysubmitallstudentresult'),
    path('primaryunsubmitallstudentresult/',primary_unsubmitallstudentresult_view , name='primarysubmitallstudentresult'),
    
    path('<str:Classname>/<int:id>/annualresult_computation/',annualresult_computation , name='annualresult_computation'),
    path('primaryannualresultcomputation/',primary_annual_result_computation_view , name='annualresultcomputation'),
    path('annualresultcomputation/',annual_result_computation_view , name='annualresultcomputation'),
    path('publishannualresults/',publish_annual_results , name='publishannualresults'),
    path('unpublishannualresults/',unpublish_annual_results , name='unpublishannualresults'),
    
	# Admin urls
    path('schoolresults/',schoolresult_view , name='schoolresults'),
    path('getprimaryclasspublishedResults/',getprimaryclasspublishedResults , name='getprimaryclasspublishedResults'),
    path('getclasspublishedResults/',getclasspublishedResults , name='getclasspublishedResults'),
	path('schoolannualresult/',schoolannualresult_view, name='schoolannualresult'),
    path('getclassannualpublishedResults/',getclassannualpublishedResults, name='getclassannualpublishedResults'),
]