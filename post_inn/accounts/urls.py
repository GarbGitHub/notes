from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path, reverse_lazy
import accounts.views as accounts

app_name = 'authapp'

urlpatterns = [
    path('login/', accounts.login, name='login'),
    path('logout/', accounts.logout, name='logout'),
    path('register/', accounts.register, name='register'),
    path('edit/', accounts.EditUserUpdateView.as_view(), name='edit'),
    path('result/', accounts.result, name='result'),
    path('edit/password/', accounts.EditUserPasswordUpdateView.as_view(), name='edit_password'),
    path('verify/<str:email>/<str:activation_key>/', accounts.verify, name='verify'),
    path('verify_update/', accounts.verify_update, name='verify_update'),

    # Форма сброса пароля
    path('password_reset', accounts.password_reset_request, name='password_reset'),

    # форма для ввода нового пароля
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="accounts/register_base.html",
             success_url='complete/'
         ),
         name='password_reset_confirm'),

    # уведомление о смене пароля
    path('reset/<uidb64>/<token>/complete/',
         accounts.UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete')
]
