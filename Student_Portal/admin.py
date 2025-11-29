from django.contrib import admin
from.models import *


admin.site.register(AcademicSession)
admin.site.register(Term)
admin.site.register(Subjectallocation)
admin.site.register(Excelfiles)
admin.site.register(Newsletter)
admin.site.register(Assignments)


@admin.register(Students_Pin_and_ID)
class Students_Pin_and_IDAdmin(admin.ModelAdmin):
    list_display=('student_name','student_id','get_current_class_display')
    ordering=('student_name',)
    search_fields=('student_name','student_id')
    list_filter=('student_name',)

    def get_current_class_display(self, obj):
        """Display the most recent class enrollment"""
        current_class = obj.get_current_class()
        return current_class.Class if current_class else "No Enrollment"
    
    get_current_class_display.short_description = 'Current Class'


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'student_class', 'academic_session', 'is_active', 'enrollment_date')
    ordering = ('-academic_session__session', 'student__student_name')
    search_fields = ('student__student_name', 'student_class__Class', 'academic_session__session')
    list_filter = ('student_class', 'academic_session', 'is_active')
    list_editable = ('is_active',)
    date_hierarchy = 'enrollment_date'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display=('subject_name','subject_code')
    ordering=('subject_name','subject_code')
    search_fields=('subject_name','subject_code')
    list_filter=('subject_name','subject_code')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display=('Class',)
    ordering=('Class',)
    search_fields=('Class',)
    list_filter=('Class',)


@admin.register(Student_Result_Data)
class Student_Result_DataAdmin(admin.ModelAdmin):
    list_display = ('Student_name', 'Position', 'display_Class', 'Average', 'Term', 'AcademicSession')
    ordering = ('Student_name', 'Position', 'Average')
    search_fields = ('Student_name__student_name', 'Position', 'Average')
    list_filter = ('Term', 'AcademicSession', 'Position')

    def display_Class(self, obj):
        """Get the class from the student's enrollment for this session"""
        enrollment = StudentEnrollment.objects.filter(
            student=obj.Student_name, 
            academic_session=obj.AcademicSession
        ).first()
        return enrollment.student_class.Class if enrollment else "No Enrollment"

    display_Class.short_description = 'Class'

@admin.register(PrimaryResult)
class PrimaryResultAdmin(admin.ModelAdmin):
    list_display = ('students_result_summary','get_student_class', 'Subject')
    ordering = ('students_result_summary', 'Subject')
    search_fields = ('students_result_summary__Student_name__student_name', 'Subject__subject_name')
    list_filter = ('Subject__subject_name', 'students_result_summary__Term', 'students_result_summary__AcademicSession')

    def get_student_class(self, obj):
        """Get the class from the student's enrollment for the result's session"""
        if obj.students_result_summary and obj.students_result_summary.AcademicSession:
            enrollment = StudentEnrollment.objects.filter(
                student=obj.students_result_summary.Student_name, 
                academic_session=obj.students_result_summary.AcademicSession
            ).first()
            return enrollment.student_class.Class if enrollment else "No Enrollment"
        return "No Session"

    get_student_class.short_description = 'Student Class'

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('students_result_summary','get_student_class', 'Subject')
    ordering = ('students_result_summary', 'Subject')
    search_fields = ('students_result_summary__Student_name__student_name', 'Subject__subject_name')
    list_filter = ('Subject__subject_name', 'students_result_summary__Term', 'students_result_summary__AcademicSession')

    def get_student_class(self, obj):
        """Get the class from the student's enrollment for the result's session"""
        if obj.students_result_summary and obj.students_result_summary.AcademicSession:
            enrollment = StudentEnrollment.objects.filter(
                student=obj.students_result_summary.Student_name, 
                academic_session=obj.students_result_summary.AcademicSession
            ).first()
            return enrollment.student_class.Class if enrollment else "No Enrollment"
        return "No Session"

    get_student_class.short_description = 'Student Class'

@admin.register(AnnualStudent)
class AnnualStudentAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'TotalScore', 'Average', 'Position', 'academicsession', 'published')
    ordering = ('Student_name__student_name', 'TotalScore', 'Average', 'Position')
    search_fields = ('Student_name__student_name', 'TotalScore', 'Average', 'Position', 'academicsession__session_name')
    list_filter = ('academicsession', 'published')

    # Helper method to display the related student name in the admin panel
    def get_student_name(self, obj):
        return obj.Student_name.student_name
    get_student_name.short_description = "Student Name"

@admin.register(AnnualResult)
class AnnualResultAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'get_subject_name', 'FirstTermTotal', 'SecondTermTotal', 'ThirdTermTotal', 'Total', 'Average', 'Grade', 'published')
    ordering = ('Student_name__Student_name__student_name', 'Subject__subject_name')
    search_fields = ('Student_name__Student_name__student_name', 'Subject__subject_name', 'Grade', 'Remark')
    list_filter = ('Subject__subject_name', 'published', 'Student_name__academicsession')

    # Helper method to display the related student name in the admin panel
    def get_student_name(self, obj):
        return obj.Student_name.Student_name.student_name
    get_student_name.short_description = "Student Name"

    # Helper method to display the related subject name in the admin panel
    def get_subject_name(self, obj):
        return obj.Subject.subject_name
    get_subject_name.short_description = "Subject Name"