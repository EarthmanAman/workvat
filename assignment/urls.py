"""workvat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_downloadview import ObjectDownloadView
from . views import (
	index,
    addAssignment,
    updateAssignment,
    deleteAssignment,

    userAssignments,
    adminAssignments,

    accept,
    completed,
    counter,
    services,
    singleAssignment,

    assignmentChange,
    changes,
	)
from . models import UserAssignment, AssignmentMedia

download = ObjectDownloadView.as_view(model=UserAssignment, file_field='file')
downloadFinished = ObjectDownloadView.as_view(model=AssignmentMedia, file_field='file')
app_name = "assignment"

urlpatterns = [
    path('', index, name="index"),
    path('assignment/add/', addAssignment, name="addAssignment"),
    path('assignment/<int:assignment_id>/update/', updateAssignment, name="updateAssignment"),
    path('assignment/<int:assignment_id>/delete/', deleteAssignment, name="deleteAssignment"),

    path('assignments/', userAssignments, name="userAssignments"),
    path('assignments/admin/', adminAssignments, name="adminAssignments"),
    path('accept/<int:assignment_id>/', accept, name="accept"),
    path('completed/<int:assignment_id>/', completed, name="completed"),
    path('counter/', counter, name="counter"),

    path('services/', services, name="services"),
    path('assignment/<int:assignment_id>/', singleAssignment, name="singleAssignment"),

    path('assignment/change/', assignmentChange, name="assignmentChange"),
    path('changes/', changes, name="changes"),

    path('download/<int:pk>/', download, name="download_assignment"),
    path('downloadFinish/<int:pk>/', downloadFinished, name="downloadFinished"),
]
