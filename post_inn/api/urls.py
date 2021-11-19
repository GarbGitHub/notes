from rest_framework.routers import DefaultRouter
from api.views import NoteViewSet, UserViewsSet

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')
router.register('users', UserViewsSet, basename='users')
urlpatterns = router.urls
