from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User


def signup(request):
    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        user = User(username=email, first_name=firstName, last_name=lastName, email=email)
        user.set_unusable_password()
        user.is_active = False
        user.save()

        # Send an email to the user with the token:
        mail_subject = 'Activate your account.'
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = "{0}/accounts/activate/{1}/{2}".format("https://workvat.com", uid, token)
        message = "Hello {0},\n {1}".format(user.first_name, activation_link)
        to_email = email
        email = EmailMessage(mail_subject, message, 'info@workvat.com', to=[to_email])
        email.send()
        return render(request, './confirm_email.html')
    return redirect("assignment:index")

def activate(request, uidb64, token):
    if request.method == "POST":
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password == password2:
            user = request.user
            user.set_password(password)
            user.save()
            login(request, user)
            # update_session_auth_hash(request, user) # Important, to update the session with the new password
            return redirect("assignment:index")
        else:
            return render(request, 'activation.html')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # activate user and login:
        user.is_active = True
        user.save()
        login(request, user)

        # form = PasswordChangeForm(request.user)
        return render(request, 'activation.html')

    else:
        return HttpResponse('Activation link is invalid!')



def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        userIn = authenticate(username=username, password=password)
        if userIn:
            login(request, userIn)
            next_endpoint = request.GET.get("next")
            return redirect("/")
    return render(request, './login.html')


def logout_user(request):
    logout(request)
    return redirect("/")

def contact(request):
    template_name = "./contact.html"
    send = False
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            firstName = user.first_name
            lastName = user.last_name
            email = user.email
        else:
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            email = request.POST.get("email")
        message = request.POST.get("message")
        mail_subject = request.POST.get("subject")
        zzzzzzzzzz
        message = "Customer Name: {} {}\nCustomer Email : {} \n Message {}".format(firstName, lastName, email, message)
        to_email = email
        email = EmailMessage(mail_subject, message, to=['info@workvat.com'])
        email.send()
        # send_mail(mail_subject, message, email, ['hashimathman@gmail.com'], fail_silently=False,)
        send = True
    context = {'send':send}
    return render(request, template_name, context)

def about(request):
    template_name = "./about.html"
    return render(request, template_name)

@login_required
def adminList(request):
    template_name = "./adminList.html"
    return render(request, template_name)






