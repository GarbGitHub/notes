from django.urls import path
import notes.views as notes

app_name = 'notesapp'

urlpatterns = [
    path('', notes.index, name='index'),
    path('app/search/', notes.SearchResultsView.as_view(), name='search_results'),
    path('app/notes/', notes.NoteListView.as_view(), name='notes_list'),
    path('app/notes/create/', notes.NoteCreateView.as_view(), name='post_create'),
    path('app/notes/detail/<int:pk>/', notes.NoteDetailView.as_view(), name='post_detail'),
    path('app/notes/update/<int:pk>/', notes.NoteUpdateView.as_view(), name='post_update'),
    path('app/notes/basket/', notes.NoteBasketListView.as_view(), name='posts_basket_list'),
    path('app/notes/basket/add/<int:pk>', notes.NoteBasketDelUpdateView.as_view(), name='post_basket_add'),
    path('app/notes/basket/detail/<int:pk>', notes.NoteBasketDetailView.as_view(), name='post_basket_detail'),
    path('app/notes/basket/return/<int:pk>', notes.NoteReturnActiveUpdateView.as_view(), name='post_basket_return'),
    path('app/notes/basket/delete/<int:pk>/', notes.NoteBasketDeleteView.as_view(), name='post_basket_delete'),
    path('app/notes/favorites/', notes.NoteFavoriteListView.as_view(), name='posts_favorites')
]
