from django.urls import path
import fordev.views as fordevs

app_name = 'fordevapp'

urlpatterns = [
    path('', fordevs.ForDevListView.as_view(), name='list'),
    path('page/<int:pk>', fordevs.ForDevDetailView.as_view(), name='page')
]