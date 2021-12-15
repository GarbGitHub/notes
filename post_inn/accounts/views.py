from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import UpdateView
from accounts.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from accounts.forms import DivErrorList, UserLoginForm, UserRegisterForm, UserEditForm, UserPasswordEditForm


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))

    title = 'Выполнить вход'
    login_form = UserLoginForm(data=request.POST or None,
                               error_class=DivErrorList)  # Все данные из формы полученные методом POST

    _next = request.GET['next'] if 'next' in request.GET.keys() else ''

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

    context = {'title_page': title,
               'form': login_form,
               'next': _next}

    return render(request, 'accounts/register_base.html', context)


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

    context['form'] = register_form
    return render(request, 'accounts/register_base.html', context)


class EditUserPasswordUpdateView(SuccessMessageMixin, UpdateView):
    success_message = "Успешно изменён пароль"
    model = User
    template_name = 'accounts/edit.html'

    def get_form(self, form_class=UserPasswordEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(self.request.user.password, error_class=DivErrorList, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Пароль'
        return context

    def get_success_url(self):
        return reverse_lazy('notesapp:notes_list')

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class EditUserUpdateView(SuccessMessageMixin, UpdateView):
    success_message = "Профиль отредактирован"
    model = User
    template_name = 'accounts/edit.html'

    def get_form(self, form_class=UserEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Профиль'
        return context

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('notesapp:notes_list')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
