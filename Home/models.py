from django.db import models
from ckeditor.fields import RichTextField


class School(models.Model):
	Schoolid=models.IntegerField()
	Schoollogo=models.ImageField(upload_to='assets/Schoollogo', blank=True)
	Schoolname= models.CharField(max_length= 300, blank=True)
	SchoolPhonenumber= models.CharField(max_length= 300, blank=True)
	Schoolmotto= models.CharField(max_length= 300, blank=True)
	Schoollocation= models.CharField(max_length= 300, blank=True)
	Facebookpage= models.CharField(max_length= 300, blank=True)
	Twitterpage= models.CharField(max_length= 300, blank=True)
	Whatsapp= models.CharField(max_length= 300, blank=True)
	Emailaddress= models.CharField(max_length= 300, blank=True)
	
	def __str__(self):
		return str(self.Schoolname)
		
	@property
	def imageURL(self):
		try:
			url= self.Schoollogo.url
		except:
			url=''
		return url
	
class schoolSection(models.Model):
	section = models.CharField(max_length= 300, blank=True)

	def __str__(self):
		return str(self.section)

class Management(models.Model):
	SN = models.IntegerField(blank=True)
	Profileimage = models.ImageField(upload_to='assets', blank=True)
	Profilename = models.CharField(max_length= 300, blank=True)
	Role= models.CharField(max_length= 300, blank=True)
	Phonenumber= models.CharField(max_length= 300, blank=True)
	Emailaddress= models.CharField(max_length= 300, blank=True)
	Facebookpage= models.CharField(max_length= 300, blank=True)
	Twitterpage= models.CharField(max_length= 300, blank=True)
	Whatsapp= models.CharField(max_length= 300, blank=True)
	
	def __str__(self):
		return str(self.Profilename)
	
	def managementimageURL(self):
		try:
			url= self.Profileimage.url
		except:
			url=""
		return url
	

class TopTeacher(models.Model):
	SN = models.IntegerField(blank=True)
	Teacher_section = models.ForeignKey(schoolSection,on_delete=models.CASCADE , blank = True,null=True)
	Profileimage=models.ImageField(upload_to='assets', blank=True)
	Profilename= models.CharField(max_length= 300, blank=True)
	Role= models.CharField(max_length= 300, blank=True)
	Phonenumber= models.CharField(max_length= 300, blank=True)
	Emailaddress= models.CharField(max_length= 300, blank=True)
	Facebookpage= models.CharField(max_length= 300, blank=True)
	Twitterpage= models.CharField(max_length= 300, blank=True)
	Whatsapp= models.CharField(max_length= 300, blank=True)
	
	def __str__(self):
		return str(self.Profilename)
	
	def TopTeachersimageURL(self):
		try:
			url= self.Profileimage.url
		except:
			url=""
		return url

		
class Header(models.Model):
	About=RichTextField(blank=True,null=True)
	Aims_and_Objectives= RichTextField(blank=True,null=True)
	Vision=models.TextField(blank=True,null=True)
	Mission=models.TextField(blank=True,null=True)
	
	def snippet(self):
		return self.About[:220] + '...'

class PhotoGallery(models.Model):
	Photo=models.ImageField(upload_to='assets/photogallery')
	Description= models.CharField(max_length= 300, blank=False)
	
	def __str__(self):
		return str(self.Description)

	@property
	def imageURL(self):
		try:
			url= self.Photo.url
		except:
			url=''
		return url

class UpcomingEvents(models.Model):
	Flier=models.ImageField(upload_to='assets/eventfliers', blank=True)
	Eventtitle= models.CharField(max_length= 300, blank=True)
	EventTopic= models.CharField(max_length= 300, blank=True)
	Eventspeaker_Chairman= models.CharField(max_length= 300, blank=True)
	Eventdate= models.CharField(max_length= 300, blank=True)
	Eventtime= models.CharField(max_length= 300, blank=True)
	Eventvenue= models.CharField(max_length= 300, blank=True)
	
	def __str__(self):
		return str(self.Eventtitle)
	
	@property
	def EventimageURL(self):
		try:
			url= self.Flier.url
		except:
			url=""
		return url
		
class FAQ(models.Model):
	questionnumber=models.CharField(max_length= 300, blank=True,help_text="use alphabets like one , two & three")
	Questions= models.CharField(max_length= 300, blank=True)
	Answer= models.CharField(max_length= 300, blank=True)
	
	def __str__(self):
		return str(self.Questions)

class ParentsReview(models.Model):
	Profileimage=models.ImageField(upload_to='assets/parentsProfileimages', blank=True )
	Name=models.CharField(max_length= 300, blank=True)
	Occupation= models.CharField(max_length= 300, blank=True)
	Review= models.TextField(blank=True)
	
	def __str__(self):
		return str(self.Name)
	
	@property
	def ParentsprofileimageURL(self):
		try:
			url= self.Profileimage.url
		except:
			url=""
		return url
	
class Subscription(models.Model):
	Email= models.EmailField(blank = True,null=True)
	
	def __str__(self):
		return str(self.Email)
	
class Contact(models.Model):
	name = models.CharField(max_length=100)
	message = models.CharField(max_length=80)
	email = models.EmailField()

	def __str__(self):
		return str(self.email)