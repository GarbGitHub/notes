from rest_framework.routers import DefaultRouter
from api.views import NoteViewSet, UserViewsSet, NoteBasketViewSet

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')
router.register('basket', NoteBasketViewSet, basename='basket')
router.register('users', UserViewsSet, basename='users')
urlpatterns = router.urls
