from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout


def auth(request):
    return render(request, 'auth_app/auth.html')


def signup(request):
    if request.method == 'GET':
        return redirect('auth')
    if request.method == 'POST':

        username = request.POST.get('username', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        password = request.POST.get('password', None)
        if username is None or password is None:
            return redirect('auth')

        user = User.objects.create_user(
            username,
            username,
            password,
            is_active=False,
            first_name=first_name,
            last_name=last_name)

        current_site = get_current_site(request)
        mail_subject = 'Активируйте свой аккаунт'
        message = render_to_string('auth_app/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(
            mail_subject, message, to=[username]
        )
        email.send()
        return render(request, 'auth_app/message.html',
                      {'message': 'Пожалуйста, подтвердите свой email адрес для завершения регистрации'})
    return redirect('auth')


def login_view(request):
    if request.method == 'GET':
        return redirect('auth')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username is None or password is None:
            return redirect('auth')
        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('auth')
        login(request, user)
    return redirect('tests')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        message = 'Ваш email адрес подтвержден. Теперь вы можете войти в свой аккаунт.'
    else:
        message = 'Проверьте правильность ссылки активации аккаунта'

    return render(request, 'auth_app/message.html', {'message': message})


def logout_view(request):
    logout(request)
    return redirect('auth')
