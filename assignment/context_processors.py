from . models import AssignmentType

def assignmentTypes(request):
	types = AssignmentType.objects.all().order_by("-pk")
	return {'assignmentTypes': types}
    
