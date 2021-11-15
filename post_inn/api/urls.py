# from django.urls import path
from rest_framework.routers import DefaultRouter
# from rest_framework.urlpatterns import format_suffix_patterns
from api.views import NoteViewSet, UserViewsSet

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')
# router.register('users', UserViewSet, basename='users')
router.register('users', UserViewsSet, basename='users')
urlpatterns = router.urls

# urlpatterns = [
#     path('notes/', NoteLisView.as_view()),
#     path('notes/<int:pk>/', NoteDetailView.as_view(), name='notes-detail'),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)

# notes_list = NoteViewSet.as_view({
#     'get': 'list',
#     'post': 'create'}
# )
# notes_detail = NoteViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# urlpatterns = [
#     path('notes/', notes_list,  name='notes-list'),
#     path('notes/<int:pk>/', notes_detail, name='notes-detail'),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)
