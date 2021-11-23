from django.urls import path
import fordev.views as fordevs

app_name = 'fordev'

urlpatterns = [
    path('list/', fordevs.FordevListView.as_view(), name='fordev_list'),
    path('detail/<int:pk>', fordevs.FordevDetailView.as_view(), name='fordev_page')
]