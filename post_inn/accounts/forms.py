from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.hashers import check_password
from accounts.models import User


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''

        return '%s' % ''.join(
            ['%s' % e for e in self])


class UserLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Не верный пароль",
        'inactive': "Вы не подтвердили регистрацию по ссылке для %(username)s",
        'not_user': "Пользователь %(username)s не существует",
        'value_err': "ValueError %(code_err)s",
    }

    class Meta:  # параметры для создаваемого класса
        model = User  # модель с которой работает класс
        fields = ('email', 'password')  # необходимые поля

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['autocomplete'] = 'username'
            if field_name == 'password':
                field.widget.attrs['autocomplete'] = 'current-password'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # self.user_cache = authenticate(self.request, username=username, password=password)
            # if self.user_cache is None:
            try:
                user_temp = User.objects.get(email=username)

                user_pass = user_temp.password
                print(user_pass)

                if not user_temp.is_active:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                        params={'username': username},
                    )

                elif not check_password(password, user_pass):
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': username},
                    )

            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    self.error_messages['not_user'],
                    code='not_user',
                    params={'username': username},
                )

            except ValueError:
                raise forms.ValidationError(
                    self.error_messages['value_err'],
                    code='value_err',
                    params={'code_err': 'Не верный формат данных'},
                )

        return self.cleaned_data


class UserRegisterForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают",
    }
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput,
        help_text="Введите тот же пароль, что и выше, для проверки",
    )

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, *args, **kwargs):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        user.activation_key = User.create_activation_key(user.email)
        user.save()

        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'name':
                field.widget.attrs['autocomplete'] = 'given-name'
            if field_name == 'last_name':
                field.widget.attrs['autocomplete'] = 'family-name'


class UserPasswordEditForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают",
        'old_password_err': "Старый пароль введен не верно",
    }

    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput,
        help_text="Введите старый пароль",
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput,
        help_text="Введите тот же пароль, что и выше, для проверки",
    )

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def __init__(self, hash_password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hash_password = hash_password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        hash_old_password = self.hash_password
        if old_password and not check_password(old_password, hash_old_password):
            raise forms.ValidationError(
                self.error_messages['old_password_err'],
                code='old_password_err'
            )
        return old_password
