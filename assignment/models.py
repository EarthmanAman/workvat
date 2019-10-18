from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

class AssignmentType(models.Model):
	name = models.CharField(max_length=100)
	desc = models.TextField(blank=True, null=True)
	trend = models.BooleanField(default=False)

	averagePrice = models.FloatField(blank=True, null=True)

	def __str__(self):
		return self.name


class TypeDesc(models.Model):
	assignmentType 	= models.ForeignKey(AssignmentType, on_delete=models.CASCADE)

	name 			= models.CharField(max_length=50)
	desc 			= models.TextField()
	necessary 	 	= models.BooleanField(default=False)

	def __str__(self):
		return self.name + " " + self.assignmentType.__str__()

class UserAssignment(models.Model):
	user 			= models.ForeignKey(User, on_delete=models.CASCADE)
	assignmentType 	= models.ForeignKey(AssignmentType, on_delete=models.CASCADE)
	title 			= models.CharField(max_length=100, blank=True, null=True)
	citation 		= models.CharField(max_length=100, blank=True, null=True)
	font 			= models.CharField(max_length=100, default="Times New Roman")
	fontSize 		= models.FloatField(default=12.0)
	pages 			= models.FloatField(blank=True, null=True)
	
	expectedDate 	= models.DateField(auto_now_add=True, blank=True, null=True)
	dateRequested 	= models.DateTimeField(auto_now_add=True)
	dateCompleted 	= models.DateTimeField(blank=True,  null=True)

	desc 		 	= RichTextField(blank=True, null=True)
	file 			= models.FileField(blank=True, null=True)

	accepted 		= models.BooleanField(default= False)
	completed 		= models.BooleanField(default=False)

	is_sample 		= models.BooleanField(default=False)

	def __str__(self):
		return self.user.username + " " + self.assignmentType.__str__()

class AssignmentChange(models.Model):
	userAssignment 	= models.ForeignKey(UserAssignment, on_delete=models.CASCADE)
	title 			= models.CharField(max_length=100)
	desc 			= models.TextField() 
	done 			= models.BooleanField(default=False)

	def __str__(self):
		return self.title + " - " + self.userAssignment.__str__()

class AssignmentMedia(models.Model):
	userAssignment 	= models.OneToOneField(UserAssignment, on_delete=models.CASCADE)
	file 			= models.FileField(upload_to='assignments/')
	is_complete 	= models.BooleanField(default=False)

	def __str__(self):
		return self.userAssignment.__str__()

class Constraint(models.Model):
	assignmentType 	= models.ForeignKey(UserAssignment, on_delete=models.CASCADE, blank=True, null=True)
	name 			= models.CharField(max_length=100)
	desc 			= RichTextField()

	must 			= models.BooleanField(default=False)

	def __str__(self):
		return self.name + " - " + self.assignmentType.__str__()