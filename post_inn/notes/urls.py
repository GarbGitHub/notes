from django.urls import path
from django.views.generic import TemplateView

import notes.views as notes

app_name = 'notesapp'

urlpatterns = [
    path('', notes.NoteListView.as_view(), name='app'),
    path("offline.html", notes.offline),
    path('search/', notes.SearchResultsView.as_view(), name='search_results'),
    path('notes/', notes.NoteListView.as_view(), name='notes_list'),
    path('notes/tags/', notes.TagsCreateView.as_view(), name='tags'),
    path('notes/tags/delete/<int:pk>/', notes.TagsDeleteView.as_view(), name='tag_delete'),
    path('notes/tags/collection/<int:pk>/', notes.NoteTagListView.as_view(), name='tag_posts_list'),
    path('notes/tags/update/<int:pk>/', notes.TagUpdateView.as_view(), name='tag_update'),
    path('notes/create/', notes.NoteCreateView.as_view(), name='post_create'),
    path('notes/detail/<int:pk>/', notes.NoteDetailView.as_view(), name='post_detail'),
    path('notes/update/<int:pk>/', notes.NoteUpdateView.as_view(), name='post_update'),
    path('notes/basket/', notes.NoteBasketListView.as_view(), name='posts_basket_list'),
    path('notes/basket/add/<int:pk>', notes.NoteBasketDelUpdateView.as_view(), name='post_basket_add'),
    path('notes/basket/detail/<int:pk>', notes.NoteBasketDetailView.as_view(), name='post_basket_detail'),
    path('notes/basket/return/<int:pk>', notes.NoteReturnActiveUpdateView.as_view(), name='post_basket_return'),
    path('notes/basket/delete/<int:pk>/', notes.NoteBasketDeleteView.as_view(), name='post_basket_delete'),
    path('notes/favorites/', notes.NoteFavoriteListView.as_view(), name='posts_favorites')
]
