from django.db import models
from Home.models import schoolSection
from django.contrib.auth.models import User
from Student_Portal.models import Students_Pin_and_ID
from Student_Portal.models import Class,Subject
from django.utils import timezone
from datetime import timedelta
import random
import secrets

ROLE_CHOICES = [
        ('Teacher', 'Teacher'),
        ('ClassTeacher', 'ClassTeacher'),
		('Admin', 'Admin'),
    ]

SECTION_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
    ]

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=2)  
	FirstName= models.CharField(max_length= 200, blank=True,default='None')
	LastName= models.CharField(max_length= 200, blank=True, default='None')
	Phone_number= models.CharField(max_length= 200, blank=True)
	Email= models.EmailField(max_length= 200, blank=True)
	teachers_id=models.CharField(max_length= 200, blank=True)
	Role= models.CharField(max_length= 200, blank=True , default="Teacher",choices=ROLE_CHOICES )
	SchoolSection= models.ForeignKey(schoolSection,on_delete=models.CASCADE,blank=True, null=True)
	subjects_taught=models.ManyToManyField(Subject)
	classes_taught=models.ManyToManyField(Class,related_name='assigned_classes')
	classFormed = models.ForeignKey(Class,on_delete=models.CASCADE, blank=True, null=True )
	Headshot=models.ImageField(upload_to='assets/TeachersProfileimages', blank=True)
	Signature=models.ImageField(upload_to='assets/TeachersSignatureimages', blank=True)
	
	
	
	def __str__(self):
		return str(self.FirstName)

	@property
	def profileimageURL(self):
		try:
			url= self.Headshot.url
		except:
			url=""
		return url
	
	def save(self, *args, **kwargs):
		if self.id:  # if object exists in database
			super().save(*args, **kwargs)  # simply update the fields
		else:  # if object is new
			while not self.teachers_id:
				random_pin = str(random.randint(1000, 9999))
				# random_password = secrets.token_urlsafe(8)
				Application_id = f"teacher/GPLA/{random_pin}"
				object_with_similar_Application_id = Teacher.objects.filter(teachers_id=random_pin)
				if not object_with_similar_Application_id:
					self.teachers_id = Application_id
					# self.teachers_password = random_password
			super().save(*args, **kwargs)


class Attendance(models.Model):
    student = models.ForeignKey(Students_Pin_and_ID, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    is_present = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} ({self.date}): {'Present' if self.is_present else 'Absent'}"

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, using=None):
        super().delete(using=using)



    





