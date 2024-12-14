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
    list_display=('student_name','student_id','student_class')
    ordering=('student_name','student_class')
    search_fields=('student_name','student_class')
    list_filter=('student_class',"student_name")


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
    list_display = ('Student_name', 'Position', 'display_Class', 'Average')
    ordering = ('Student_name', 'Position', 'Average')
    search_fields = ('Student_name__student_class','Position', 'Average')
    list_filter = ('Student_name__student_class','Student_name', 'Position', 'Average')

    def display_Class(self, obj):
        return obj.Student_name.student_class

    display_Class.short_description = 'Class'

@admin.register(PrimaryResult)
class PrimaryResultAdmin(admin.ModelAdmin):
    list_display = ('students_result_summary','get_student_class', 'Subject')
    ordering = ('students_result_summary','students_result_summary__Student_name__student_class', 'Subject')
    search_fields = ('students_result_summary__Student_name__student_class', 'Subject__subject_name')
    list_filter = ('students_result_summary__Student_name__student_class', 'Subject__subject_name')

    def get_student_class(self, obj):
        return obj.students_result_summary.Student_name.student_class

    get_student_class.short_description = 'Student Class'

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('students_result_summary','get_student_class', 'Subject')
    ordering = ('students_result_summary','students_result_summary__Student_name__student_class', 'Subject')
    search_fields = ('students_result_summary__Student_name__student_class', 'Subject__subject_name')
    list_filter = ('students_result_summary__Student_name__student_class', 'Subject__subject_name')

    def get_student_class(self, obj):
        return obj.students_result_summary.Student_name.student_class

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
    ordering = ('students_result_data__Student_name__student_name', 'Subject__subject_name')
    search_fields = ('students_result_data__Student_name__student_name', 'Subject__subject_name', 'Grade', 'Remark')
    list_filter = ('Subject__subject_name', 'published')

    # Helper method to display the related student name in the admin panel
    def get_student_name(self, obj):
        return obj.students_result_data.Student_name.student_name
    get_student_name.short_description = "Student Name"

    # Helper method to display the related subject name in the admin panel
    def get_subject_name(self, obj):
        return obj.Subject.subject_name
    get_subject_name.short_description = "Subject Name"