from django.urls import path
import fordev.views as fordevs

app_name = 'fordevapp'

urlpatterns = [
    path('', fordevs.ForDevListView.as_view(), name='list'),
    path('1/', fordevs.ForDevListView.as_view(), name='list'),
    path('<int:cat_pk>/page/<int:pk>', fordevs.ForDevDetailView.as_view(), name='page')
]