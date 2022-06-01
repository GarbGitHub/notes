import logging
import smtplib

from django.contrib import auth
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
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
from post_inn import get_config, settings
from accounts.forms import DivErrorList, UserLoginForm, UserRegisterForm, UserEditForm, UserPasswordEditForm

logger = logging.getLogger('main')


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

            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])

            else:
                return HttpResponseRedirect(reverse('notesapp:notes_list'))

    return render(request, 'accounts/register_base.html', context)


def logout(request):
    auth.logout(request)
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
                logger.info(f'Зарегистрировался новый пользователь {email}')
                return HttpResponseRedirect(reverse('auth:result'))

            else:
                message = f'Мы не смогли отправить ссылку на {email} для подтверждения регистрации'
                logger.error(message)
                request.session['message'] = message
                return HttpResponseRedirect(reverse('auth:result'))

    else:
        register_form = UserRegisterForm()

    context['form'] = register_form
    return render(request, 'accounts/register_base.html', context)


def result(request):
    """Выводим результат регистрации"""

    context = {
        'title_page': 'Результат регистрации',
        'description': 'Результат регистрации',
        'static_get_param': get_config.GET_CONFIG
    }

    try:
        if request.session.get('message'):
            context['message'] = request.session.get('message')
            del request.session['message']

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
        return render(request, 'accounts/register_base.html', context)


def send_verify_mail(user):
    """
    Подтвердить регистрацию по email
    :param user:
    :return: количество успешно доставленных сообщений (которое может быть 0 или 1)
    """

    try:
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.email}'
        message = f'Для подтверждения учетной записи {user.email}, на сайте {settings.DOMAIN_NAME} - пройдите по ссылке: ' \
                  f'{settings.DOMAIN_NAME}{verify_link}'

        # fail_silently = False, в случае неудачной отправки, генерируется ошибка smtplib.SMTPException)
        result_send_message = send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        logger.info(f'Пользователю {user.email} отправлена ссылка для подтверждения регистрации')
        return result_send_message

    except smtplib.SMTPException as e:
        logging.error(f'При отправке письма произошла ошибка', e)

    except Exception:
        logging.error(f'При отправке письма произошло исключение', exc_info=True)
        return 0


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
        logging.error(f'При верификации пользователя произошло исключение {err.args[0]}', exc_info=True)
        return render(request, 'accounts/register_base.html', context)


def verify_update(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))

    context = {'title_page': 'Новая ссылка'}
    try:
        email = request.session['user_email']
        user = User.objects.get(email=email)

        if user:
            print('Старый ключ', user.activation_key)
            print('Старое время', user.activation_key_expires)

            # New key and date
            user.activation_key = User.create_activation_key(user.email)
            user.activation_key_expires = User.create_key_expiration_date()
            user.save()

            del request.session['user_email']
            print('Новый ключ', user.activation_key)
            print('Новое время', user.activation_key_expires)

            if send_verify_mail(user) > 0:
                request.session['message'] = f'Проверьте почту {email} для завершения регистрации'
                return HttpResponseRedirect(reverse('auth:result'))

            else:
                request.session['message'] = f'Мы не смогли отправить ссылку на {email} для подтверждения регистрации'
                return HttpResponseRedirect(reverse('auth:result'))

        return render(request, 'accounts/register_base.html', context)

    except Exception as err:
        print('исключение')
        context['title_dialog'] = f'Отказано!'
        context['message'] = f'Error: {err.args[0]}'
        context['verify_error'] = True
        messages.success(request, context['title_dialog'])
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

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('notesapp:notes_list')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
