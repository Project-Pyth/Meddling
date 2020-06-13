from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
# Create your views here.
'''
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage,send_mail
from django.contrib.sessions.models import Session
# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import View

from accounts.models import Profile
from accounts.token import account_activation_token


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('myapp:index')
        else:
             messages.info(request, "invalid credentials")
             return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username= request.POST['username']
        Email = request.POST['Email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('accounts:register')
            elif User.objects.filter(email=Email).exists():
                messages.info(request,'email taken')
                return redirect('accounts:register')
            else:
                user= User.objects.create_user(first_name=first_name,
                                      last_name =last_name ,
                                      username =username,
                                      email =Email,
                                      password =password )

                user.is_active = False  # Deactivate account till it is confirmed
                user.save()

                print('user creater')

                current_site = get_current_site(request)
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                                           })
                mail_subject = 'Activate your Meddeling Account.'
                to_email = request.POST['Email']
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                messages.info(request, 'Please confirm your email address to complete the registration.')
                return render(request, 'accounts/register.html')
                # return render(request, 'acc_active_sent.html')
        else:
            messages.info(request, 'Password not matching')
            return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')


def logout(request):
        auth.logout(request)
        return render('myapp:index')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request, 'accounts/thanks.html')
    else:
        messages.info(request, 'Activation link is invalid!')
        return render(request, 'accounts/register.html')

    #dashboard function

def prev(request):

    return render(request, 'accounts/previous.html')


'''


