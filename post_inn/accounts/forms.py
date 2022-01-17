from django.contrib.auth.forms import AuthenticationForm
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
        return '<div class="alert alert-danger" role="alert">%s</div>' % ''.join(
            ['<div class="error">%s</div>' % e for e in self])


class UserLoginForm(AuthenticationForm):
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
        'password_mismatch': "Passwords don\'t match.",
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
        self.hash_password = hash_password
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name != 'old_password':
                field.widget.attrs['autocomplete'] = 'new-password'
            else:
                field.widget.attrs['autocomplete'] = 'current-password'

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
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return old_password
