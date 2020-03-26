from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from accounts.models import Testimonial
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from payment.models import AssignmentPayment

from . forms import UserAssignmentForm
from . models import (
	AssignmentChange,
	AssignmentMedia,
	AssignmentType,
	TypeDesc,
	UserAssignment,
	)


def index(request):
	template_name = "./index.html"
	users = User.objects.count()
	assignmentsCount = UserAssignment.objects.count()
	assignments = UserAssignment.objects.filter(is_sample=True)
	completedAssignmentsCount = UserAssignment.objects.filter(completed=True).count()
	testimonials = Testimonial.objects.all()
	userAv = request.session.get("userAv")
	context = {
			 "users":users,
			 "assignments":assignments,
			 "assignmentsCount":assignmentsCount, 
			 "completedAssignmentsCount":completedAssignmentsCount,
			 'testimonials':testimonials,
			 "userAv":userAv
			 }
	return render(request, template_name, context)

def services(request):
	template_name = "./services.html"
	servicesIn = AssignmentType.objects.all()
	testimonials = Testimonial.objects.all()
	page = request.GET.get('page', 1)

	paginator = Paginator(servicesIn, 12)
	try:
		services = paginator.page(page)
	except PageNotAnInteger:
		services = paginator.page(1)
	except EmptyPage:
		services = paginator.page(paginator.num_pages)
	context = {"services":services, "testimonials":testimonials}
	return render(request, template_name, context)

@login_required
def singleAssignment(request, assignment_id):
	template_name = "./singleAssignment.html"
	assignment = UserAssignment.objects.get(pk=assignment_id)
	host = request.get_host()
	total = assignment.assignmentpayment.userPrice * assignment.pages
	paypal_dict = {
		'business': settings.PAYPAL_RECEIVER_EMAIL,
		# 'amount': '%.2f' % total,
		'amount': '1',
		'item_name': 'Order {}'.format(assignment_id),
		'invoice' : str(assignment_id),
		'currency_code': 'USD',
		'notify_url':'http://{}{}'.format(host, reverse('paypal-ipn')),
		'return_url': 'http://{}{}'.format(host, reverse('payment:payment_done', kwargs={'assignmentId':assignment_id})),
		'cancel_return':'http://{}{}'.format(host, reverse('payment:payment_canceled', kwargs={'assignmentId':assignment_id})),
	}
	form = PayPalPaymentsForm(initial=paypal_dict)

	if request.method == "POST":
		file = request.FILES.get("file")
		try:
			media = assignment.assignmentmedia
			media.file = file
			media.save()
		except:
			assignmentMedia = AssignmentMedia(userAssignment=assignment, file=file)
			assignmentMedia.save()
		assignment.completed = True
		assignment.save()

	context = {"assignment":assignment, 'form':form}
	return render(request, template_name, context)

@login_required
def addAssignment(request):
	template_name = "./addAssignment.html"
	assignmentsTypes = AssignmentType.objects.all()
	if request.method == "POST":
		form = UserAssignmentForm(request.POST)
		if form.is_valid():
			desc = form.cleaned_data['desc']
		assignmentTypeId = int(request.POST.get("assignmentType"))
		assignmentType = assignmentsTypes.get(pk=assignmentTypeId)
		title = request.POST.get("title")
		# desc = request.POST.get("desc")
		expectedDate = request.POST.get("expectedDate")
		userPrice = int(request.POST.get("userPrice"))
		citation = request.POST.get("citation")
		fontType = request.POST.get("fontType")
		fontSize = float(request.POST.get("fontSize"))
		currency = request.POST.get("currency")
		file = request.FILES.get("file")
		pages = request.POST.get("pages", None)
		assignment = UserAssignment(
			user=request.user,
			assignmentType=assignmentType,
			title=title,
			desc=desc,
			expectedDate=expectedDate,
			citation=citation,
			font=fontType,
			fontSize=fontSize,
			pages = pages,
			)
		assignment.save()
		if file:
			assignment.file = file
			assignment.save()
		assignmentPay = AssignmentPayment(userAssignment=assignment, userPrice=userPrice, currency=currency)
		assignmentPay.save()
		return redirect("assignment:singleAssignment", assignment_id = assignment.id)
	else:
		form = UserAssignmentForm()

	context = {"assignmentsTypes":assignmentsTypes, "form":form}
	return render(request, template_name, context)

@login_required
def updateAssignment(request, assignment_id):

	template_name = "./update.html"
	assignmentsTypes = AssignmentType.objects.all()
	assignmentIn = UserAssignment.objects.get(pk=assignment_id)
	if request.method == "POST":
		form = UserAssignmentForm(request.POST, instance=assignmentIn)
		if form.is_valid():
			desc = form.cleaned_data['desc']
		assignmentTypeId = int(request.POST.get("assignmentType"))
		assignmentType = assignmentsTypes.get(pk=assignmentTypeId)
		title = request.POST.get("title")
		# desc = request.POST.get("desc")
		expectedDate = request.POST.get("expectedDate")
		userPrice = float(request.POST.get("userPrice"))
		citation = request.POST.get("citation")
		fontType = request.POST.get("fontType")
		fontSize = float(request.POST.get("fontSize"))
		currency = request.POST.get("currency")
		file = request.FILES.get("file", None)
		assignmentIn.assignmentType = assignmentType
		assignmentIn.user = request.user
		assignmentIn.title = title
		assignmentIn.expectedDate = expectedDate
		assignmentIn.assignmentpayment.userPrice = userPrice
		assignmentIn.assignmentpayment.currency = currency
		assignmentIn.citation = citation
		assignmentIn.font = fontType
		assignmentIn.fontSize = fontSize
		if file:
			assignmentIn.file = file
		assignmentIn.save()
		assignmentIn.assignmentpayment.save()
	
		return redirect("assignment:singleAssignment", assignment_id = assignmentIn.id)
	else:
		form = UserAssignmentForm(instance=assignmentIn)

	context = {"assignmentsTypes":assignmentsTypes, "form":form, 'assignment':assignmentIn}
	return render(request, template_name, context)

@login_required
def deleteAssignment(request, assignment_id):
	assignment = UserAssignment.objects.get(pk=assignment_id)
	assignment.delete()
	url = request.META.get('HTTP_REFERER')
	return redirect("assignment:userAssignments")

@login_required
def userAssignments(request):
	template_name = "./userAssignments.html"
	userAssignmentsIn = request.user.userassignment_set.all().order_by("-pk")
	assignment = None
	if request.method == "POST":
		assignment_id = int(request.POST.get("id"))
		assignment = userAssignmentsIn.get(pk=assignment_id)

	page = request.GET.get('page', 1)

	paginator = Paginator(userAssignmentsIn, 10)
	try:
		assignments = paginator.page(page)
	except PageNotAnInteger:
		assignments = paginator.page(1)
	except EmptyPage:
		assignments = paginator.page(paginator.num_pages)
	context = {"assignments":assignments, "assignment":assignment}
	return render(request, template_name, context)

@login_required
def adminAssignments(request):
	template_name = "./adminAssignments.html"
	assignmentsList = UserAssignment.objects.all().order_by("-expectedDate")
	assignment = None
	if request.method == "POST":
		assignment_id = int(request.POST.get("id"))
		assignment = assignmentsList.get(pk=assignment_id)
	page = request.GET.get('page', 1)

	paginator = Paginator(assignmentsList, 10)
	try:
		assignments = paginator.page(page)
	except PageNotAnInteger:
		assignments = paginator.page(1)
	except EmptyPage:
		assignments = paginator.page(paginator.num_pages)
	context = {"assignments": assignments}
	return render(request, template_name, context)

@login_required
def accept(request, assignment_id):
	assignment = UserAssignment.objects.get(pk=assignment_id)
	assignment.accepted = not assignment.accepted
	assignment.save()
	url = request.META.get('HTTP_REFERER')
	return redirect(url)

@login_required
def completed(request, assignment_id):
	assignment = UserAssignment.objects.get(pk=assignment_id)
	assignment.completed = not assignment.completed
	if assignment.completed == True:
		assignment.dateCompleted = timezone.now() 
	assignment.save()
	url = request.META.get('HTTP_REFERER')
	return redirect(url)


@login_required
def counter(request):
	assignment_id = int(request.POST.get("id"))
	counterPrice = int(request.POST.get("counterPrice"))
	assignment = UserAssignment.objects.get(pk=assignment_id)
	assignment.counterPrice = counterPrice
	assignment.save()
	url = request.META.get('HTTP_REFERER')
	return redirect(url)

@login_required
def assignmentChange(request):
	if request.method == "POST":
		title = request.POST.get('title')
		desc = request.POST.get('desc')
		assignment_id = int(request.POST.get('id'))
		assignment = get_object_or_404(UserAssignment, pk=assignment_id)
		if assignment.assignmentchange_set.count() < 2:
			assignmentChangeIn = AssignmentChange(userAssignment=assignment, title=title, desc=desc)
			assignmentChangeIn.save()
		elif assignment.assignmentchange_set.count() == 2:
			assignmentChangeIn = AssignmentChange(userAssignment=assignment, title=title, desc=desc, done=True)
			assignmentChangeIn.save()
		assignment.completed = False
		assignment.save()
	return redirect("assignment:singleAssignment", assignment_id=assignment.id)


@login_required
def changes(request):
	template_name = "./changes.html"
	assignments = UserAssignment.objects.all().order_by("expectedDate")
	context = {"assignments":assignments}
	return render(request, template_name, context)