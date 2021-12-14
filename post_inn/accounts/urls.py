from django.urls import path

import accounts.views as accounts

app_name = 'authapp'

urlpatterns = [
    path('login/', accounts.login, name='login'),
    path('logout/', accounts.logout, name='logout'),
    path('register/', accounts.register, name='register'),
    path('edit/', accounts.EditUserUpdateView.as_view(), name='edit'),
    path('edit/password/', accounts.EditUserPasswordUpdateView.as_view(), name='edit_password')
]