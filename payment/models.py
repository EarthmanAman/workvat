from django.db import models
from assignment.models import UserAssignment

class AssignmentPayment(models.Model):
	userAssignment 	= models.OneToOneField(UserAssignment, on_delete=models.CASCADE)
	currency 		= models.CharField(max_length=50)
	userPrice 		= models.FloatField()
	counterPrice 	= models.FloatField(blank=True, null=True)

	halfPaid 		= models.BooleanField(default=False)
	fullPaid 		= models.BooleanField(default=False)
