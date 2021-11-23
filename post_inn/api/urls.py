from rest_framework.routers import DefaultRouter
from api.views import NoteViewSet, UserViewsSet, NoteBasketViewSet, NoteFavoritesViewSet

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')
router.register('favorites', NoteFavoritesViewSet, basename='favorites')
router.register('basket', NoteBasketViewSet, basename='basket')
router.register('users', UserViewsSet, basename='users')
urlpatterns = router.urls
