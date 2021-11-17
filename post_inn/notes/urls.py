from django.urls import path

import notes.views as notes

urlpatterns = [
    path('', notes.NoteListView.as_view(), name='index'),
    path('notes/', notes.NoteListView.as_view(), name='notes_list'),
    path('notes/detail/<int:pk>/', notes.NoteDetailView.as_view(), name='post_detail'),
    path('notes/update/<int:pk>/', notes.NoteUpdateView.as_view(), name='post_update'),
    path('notes/delete/<int:pk>/', notes.NoteDeleteView.as_view(), name='post_delete'),
    path('notes/create/', notes.NoteCreateView.as_view(), name='post_create'),
]
