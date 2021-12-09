from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from accounts.forms import DivErrorList, UserLoginForm, UserRegisterForm


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))

    title = 'вход'
    login_form = UserLoginForm(data=request.POST or None,
                               error_class=DivErrorList)  # Все данные из формы полученные методом POST

    _next = request.GET['next'] if 'next' in request.GET.keys() else ''  # next=/basket/add/3/

    if request.method == 'POST' and login_form.is_valid():  # если POST
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)  # авторизован или нет

        if user and user.is_active:
            auth.login(request, user)

            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])

            else:
                return HttpResponseRedirect(reverse('notesapp:notes_list'))

    context = {'title': title,
               'login_form': login_form,
               'next': _next}

    return render(request, 'accounts/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))
    context = {'title_page': 'Регистрация нового пользователя'}
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES, error_class=DivErrorList)
        if register_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = register_form.save(commit=False)

            # Set the chosen password
            new_user.set_password(register_form.cleaned_data['password1'])

            # Save the User object
            new_user.save()
            messages.success(request, 'Успешно зарегистрирован')
            return HttpResponseRedirect(reverse('auth:login'))

    else:
        register_form = UserRegisterForm()

    context['register_form'] = register_form
    return render(request, 'accounts/register.html', context)
