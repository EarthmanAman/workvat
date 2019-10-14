from django.db import models

from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

class Testimonial(models.Model):
	user 		= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	content		= RichTextField()

	timestamp 	= models.DateField(auto_now=True)
