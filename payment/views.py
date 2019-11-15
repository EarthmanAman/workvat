from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from assignment.models import UserAssignment
from django.views.decorators.csrf import csrf_exempt

from assignment.models import UserAssignment

@csrf_exempt
def payment_done(request, assignmentId):
	template_name = './payment_done.html'
	assignment = UserAssignment.objects.get(pk=assignmentId)
	assignmentPay = assignment.assignmentpayment
	assignmentPay.fullPaid = True
	assignmentPay.save()
	return render(request, template_name)

@csrf_exempt
def payment_canceled(request):
	template_name = './payment_canceled.html'
	return render(request, template_name)



def payment_process(request, assignment_id):
	template_name = './payment_process.html'
	assignment = get_object_or_404(UserAssignment, id=assignment_id)
	host = request.get_host()

	paypal_dict = {
		'business': settings.PAYPAL_RECEIVER_EMAIL,
		'amount': '%.2f' % assignment.userPrice,
		'item_name': 'Order {}'.format(assignment_id),
		'invoice' : str(assignment_id),
		'currency_code': 'USD',
		'notify_url':'http://{}{}'.format(host, reverse('paypal-ipn')),
		'return_url': 'http://{}{}'.format(host, reverse('payment:payment_done')),
		'cancel_return':'http://{}{}'.format(host, reverse('payment:payment_canceled')),
	}
	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {'assignment':assignment, 'form':form}
	return render(request, template_name, context)
