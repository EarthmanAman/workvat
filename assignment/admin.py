from django.contrib import admin

from . models import (
	AssignmentChange,
	AssignmentMedia,
	AssignmentType,
	Constraint,
	TypeDesc,
	UserAssignment,
	)

admin.site.register(AssignmentChange)
admin.site.register(AssignmentMedia)
admin.site.register(AssignmentType)
admin.site.register(Constraint)
admin.site.register(TypeDesc)
admin.site.register(UserAssignment)
