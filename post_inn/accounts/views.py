import logging

from django.contrib import auth
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import User
from accounts.utils.send_mail import send_verify_mail, send_reset_password
from accounts.forms import DivErrorList, UserLoginForm, UserRegisterForm, UserEditForm, UserPasswordEditForm

from post_inn import get_config
from post_inn.utils import logger


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))

    login_form = UserLoginForm(data=request.POST or None, error_class=DivErrorList)
    _next = request.GET['next'] if 'next' in request.GET.keys() else ''
    context = {'title_page': 'Выполнить вход',
               'form': login_form,
               'next': _next,
               'description': 'Выполните вход, чтобы получить доступ доступ к вашим заметкам.',
               'static_get_param': get_config.GET_CONFIG
               }
    err_message = str(login_form.non_field_errors())

    if request.method == 'POST' and 'не подтвердили регистрацию' in err_message:
        context['non_verify'] = True
        request.session['user_email'] = request.POST['username']

    elif request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            logger.info(f'Авторизовался {user.email}')

            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])

            else:
                return HttpResponseRedirect(reverse('notesapp:notes_list'))

    return render(request, 'accounts/register_base.html', context)


def logout(request):
    email = User.get_user_email(request.user.pk)
    auth.logout(request)
    logger.info(f'Вышел {email}')
    return HttpResponseRedirect(reverse('auth:login'))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))

    context = {
        'title_page': 'Регистрация нового пользователя',
        'description': 'Зарегистрируйтесь, чтобы получить доступ к вашим заметкам с любых устройств.',
        'static_get_param': get_config.GET_CONFIG
    }

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES, error_class=DivErrorList)

        if register_form.is_valid():
            email = request.POST['email']
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password1'])

            if send_verify_mail(user) > 0:
                request.session['message'] = f'Проверьте почту {email} для завершения регистрации'
                user.save()
                return HttpResponseRedirect(reverse('auth:result'))

            else:
                message = f'Мы не смогли отправить ссылку на {email} для подтверждения регистрации'
                logger.info(message)
                request.session['message'] = message
                return HttpResponseRedirect(reverse('auth:result'))

    else:
        register_form = UserRegisterForm()

    context['form'] = register_form
    return render(request, 'accounts/register_base.html', context)


def result(request):
    """Выводим результат регистрации"""

    context = {
        'title_page': 'Результат',
        'description': 'Результат',
        'static_get_param': get_config.GET_CONFIG
    }

    try:
        if request.session.get('message'):
            context['message'] = request.session.get('message')
            del request.session['message']

        if request.session.get('title_dialog'):
            context['title_dialog'] = request.session.get('title_dialog')
            del request.session['title_dialog']

        else:
            context['title_dialog'] = f'Проверьте почту!'
            messages.success(request, context['title_dialog'])

        if request.user.is_authenticated or not context['message']:
            return HttpResponseRedirect(reverse('notesapp:notes_list'))

        return render(request, 'accounts/register_base.html', context)

    except Exception as err:
        context['title_dialog'] = f'Ошибка'
        context['message'] = f'Registration error: "{err.args[0]}"'
        context['verify_error'] = True
        messages.success(request, context['title_dialog'])
        logging.error(f'Исключение при регистрации пользователя:  {err.args[0]}', exc_info=True)
        return render(request, 'accounts/register_base.html', context)


def verify(request, email, activation_key):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))

    context = {'title_page': 'Верификация учетной записи пользователя'}
    try:
        user = User.objects.get(email=email)

        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            logger.info(f'Пользователь {user.email} успешно подтвердил регистрацию по почте')
            # auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            context['title_dialog'] = f'Успешно!'
            context['message'] = f'Учетная запись {user.email} подтверждена 😀'
            context['verify_success'] = True
            messages.success(request, context['title_dialog'])

        else:
            context['title_dialog'] = f'Отказано!'
            context['message'] = f'Ссылка для подтверждения регистрации учетной записи {user.email} устарела и больше ' \
                                 f'не действительна.'
            context['verify_old_link'] = True
            request.session['user_email'] = user.email
            messages.success(request, context['title_dialog'])
            logger.info(f'Пользователю {user.email} отказано в верификации, ссылка устарела')

        return render(request, 'accounts/register_base.html', context)

    except Exception as err:
        context['title_dialog'] = f'Отказано!'
        context['message'] = f'Error: {err.args[0]}'
        context['verify_error'] = True
        messages.success(request, context['title_dialog'])
        logging.error(f'Исключение при верификации пользователя:  {err.args[0]}', exc_info=True)
        return render(request, 'accounts/register_base.html', context)


def verify_update(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))

    context = {'title_page': 'Новая ссылка'}
    try:
        email = request.session['user_email']
        user = User.objects.get(email=email)

        if user:
            logger.debug('Old key', user.activation_key)
            logger.debug('Old time', user.activation_key_expires)

            # New key and date
            user.activation_key = User.create_activation_key(user.email)
            user.activation_key_expires = User.create_key_expiration_date()
            user.save()

            del request.session['user_email']
            logger.debug('New key', user.activation_key)
            logger.debug('New time', user.activation_key_expires)

            if send_verify_mail(user) > 0:
                request.session['message'] = f'Проверьте почту {email} для завершения регистрации'
                return HttpResponseRedirect(reverse('auth:result'))

            else:
                request.session['message'] = f'Мы не смогли отправить ссылку на {email} для подтверждения регистрации'
                return HttpResponseRedirect(reverse('auth:result'))

        return render(request, 'accounts/register_base.html', context)

    except Exception as err:
        context['title_dialog'] = f'Отказано!'
        context['message'] = f'Error: {err.args[0]}'
        context['verify_error'] = True
        messages.success(request, context['title_dialog'])
        logging.error(f'Исключение при верификации пользователя:  {err.args[0]}', exc_info=True)
        return render(request, 'accounts/register_base.html', context)


class EditUserPasswordUpdateView(SuccessMessageMixin, UpdateView):
    success_message = "Успешно изменён пароль"
    model = User
    template_name = 'accounts/edit_password.html'

    def get_form(self, form_class=UserPasswordEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(self.request.user.password, error_class=DivErrorList, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Пароль'
        context['static_get_param'] = get_config.GET_CONFIG
        return context

    def get_success_url(self):
        email = User.get_user_email(user_pk=self.request.user.id)
        logger.info(f' Пользователь {email} успешно сменил пароль')
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
        context['static_get_param'] = get_config.GET_CONFIG
        return context

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.request.user.id)
        return user

    def get_success_url(self):
        email = self.object.email
        name = self.object.name
        last_name = self.object.last_name
        logger.info(f'Пользователь {email} обновил профиль: {name=} {last_name=}')
        return reverse_lazy('notesapp:notes_list')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# https://www.youtube.com/watch?v=i6wNXuY8lQA
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)

        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)  # email в форме регистрации проверен на уникальность

            except ObjectDoesNotExist:
                request.session['title_dialog'] = 'Не верный email'
                request.session['message'] = f'Пользователь с адресом {email} не зарегистрирован. Письмо не отправлено!'
                logger.info(f'Исключение при восстановлении пароля: Пользователь {email} не зарегистрирован!')
                return HttpResponseRedirect(reverse('auth:result'))

            except Exception as err:
                request.session['title_dialog'] = 'Error'
                request.session['message'] = f'{err}'
                logger.error(f'При восстановлении пароля для {email} возникло исключение: {err}')
                return HttpResponseRedirect(reverse('auth:result'))

            if send_reset_password(user) > 0:
                request.session['message'] = f'Проверьте почту {email} для получения инструкции по сбросу пароля'

            else:
                request.session['title_dialog'] = f'Ошибка'
                request.session['message'] = f'Мы не смогли отправить ссылку на {email} для подтверждения регистрации'

            return HttpResponseRedirect(reverse('auth:result'))

    else:
        password_reset_form = PasswordResetForm()

    return render(request=request, template_name="accounts/password_reset.html",
                  context={"password_reset_form": password_reset_form})
