from . models import AssignmentType

def assignmentTypes(request):
	types = AssignmentType.objects.filter(trend=True).order_by("-pk")
	return {'assignmentTypes': types}
    
