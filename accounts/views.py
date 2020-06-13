from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.contrib.sessions.models import Session
# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import View

from accounts.form import UserUpdate, ProfileUpdate
from accounts.models import File, Category, UserProfile, Question, Feedback
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accounts.token import account_activation_token
import json
import urllib


def home(request):
    context = {}
    cat = Category.objects.filter(parent=None)
    context['cat'] = cat
    return render(request, "index.html", context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('accounts:index')
        else:
            messages.info(request, "invalid credentials")
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        Email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                print("username taken")
                messages.info(request, 'username taken')
                return redirect('accounts:register')
            elif User.objects.filter(email=Email).exists():
                print("email taken")
                messages.info(request, 'email taken')
                return redirect('accounts:register')
            else:
                user = User.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                email=Email,
                                                password=password)

                user.is_active = False  # Deactivate account till it is confirmed
                user.save()
                UserProfile.objects.create(user=user)
                print('user creater')

                current_site = get_current_site(request)
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activate your Meddeling Account.'
                to_email = request.POST['email']
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
    return redirect('accounts:index')


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

    # dashboard function


def pdf(request, pk=None):
    context = {}
    file = File.objects.filter(cat=pk)
    context['file'] = file
    return render(request, 'accounts/file.html', context)


def quiz(request):
    context = {}
    with urllib.request.urlopen('https://opentdb.com/api.php?amount=10&category=9&type=boolean') as url:
        document = json.loads(url.read().decode())
        data = document['results']
        context['data'] = data
        return render(request, 'accounts/quiz.html', context)


def aboutus(request):
    context = {}
    return render(request, 'accounts/aboutus.html', context)


def feedback(request):
    context = {}

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']
        feedback = Feedback(name=name, email=email, content=content)
        feedback.save()
        return redirect('accounts:index')
        messages.success(request, 'Thank you for  your feedback', context)
    return render(request, 'accounts/feedback.html')


def sub_pdf(request, pk=None):
    context = {}
    cat = Category.objects.filter(parent=pk)
    context['cat'] = cat
    return render(request, 'accounts/list.html', context)


def pdf(request, pk=None):
    context = {}
    file = File.objects.filter(cat=pk)
    context['file'] = file
    return render(request, 'accounts/file.html', context)


def profile(request):
    return render(request, 'accounts/profile.html')


def editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        p_form = ProfileUpdate(request.POST or None, request.FILES or None, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('accounts:profile')
        else:
            return redirect('accounts:editprofile')
    else:
        u_form = UserUpdate(instance=request.user)
        p_form = ProfileUpdate(instance=request.user.userprofile)
    return render(request, 'accounts/editprofile.html', {'u_form': u_form, 'p_form': p_form})


@login_required(login_url='accounts:login')
def changepass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            return HttpResponse("<h1>Congratulations... your Password  has been Changed!!!!!!</h1>")
    else:
        form = PasswordChangeForm(request.user)
    params = {
        'form': form,
    }
    return render(request, 'accounts/changepass.html', params)


# question

def category(request):
    choices = Question.CAT_CHOICES
    print(choices)
    return render(request, 'accounts/futurescope.html', {'choices': choices})


def questions(request, choices):
    print(choices)
    ques = Question.objects.all()
    print(ques)
    return render(request, 'accounts/question.html', {'ques': ques})
