from django import forms
from django.contrib.auth.models import User
from . models import UserAssignment

class UserAssignmentForm(forms.ModelForm):

    class Meta:
        model = UserAssignment
        fields = [
            # 'assignmentType',
            'desc',
            # 'file',
            # 'userPrice',
        ]

        # widgets = {
        #     "assignmentType":forms.Select(attrs={"class":"form-control"}),
        #     "desc":forms.Textarea(attrs={"class":"form-control"}),
        #     "file":forms.FileInput(attrs={"class":"form-control"}),
        #     "userPrice":forms.TextInput(attrs={"class":"form-control"}),
        # }
        # 