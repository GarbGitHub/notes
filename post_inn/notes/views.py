from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from notes.forms import NoteBasketForm, NoteEditForm, NoteReturnBasketForm
from notes.models import Note
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

PAGINATE_BY_NOTES = 7


class SearchResultsView(ListView):
    paginate_by = PAGINATE_BY_NOTES
    model = Note
    template_name = 'notes/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if len(query) == 0:
            return []
        print(query)
        objects = Note.objects.filter(Q(title__icontains=query) | Q(text__icontains=query),
                                      author=self.request.user,
                                      is_active=True)
        part = list(objects.filter(title__icontains=query)) + list(objects.filter(text__icontains=query))
        return part

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['title_page'] = 'Поиск заметок'
        if len(self.request.GET.get('q')) == 0:
            context['no_search_result'] = 'Задан пустой запрос'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NoteListView(ListView):
    paginate_by = PAGINATE_BY_NOTES
    model = Note
    template_name = 'notes/posts.html'
    context_object_name = 'posts'
    ordering = '-created'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user, is_active=True).order_by('-is_favorites', '-created')
        # return Note.objects.filter(category__pk=self.kwargs.get('pk')).order_by('-is_active')

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        # context = Note.objects.filter(author=self.request.user)
        context['title_page'] = 'Список заметок'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.id
        context['title_page'] = f'{context.get(self, self.object.title)}'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notesapp:notes_list'))
        return super().dispatch(*args, **kwargs)


class NoteUpdateView(SuccessMessageMixin, UpdateView):
    model = Note
    template_name = 'notes/post_update.html'
    success_message = "Успешно отредактировано"

    def get_form(self, form_class=NoteEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = f'Править: "{context.get(self, self.object.title)}"'
        # author_pk = context.get(self, self.object.author.pk)
        # request_user_pk = self.request.user.pk
        return context

    def get_success_url(self):
        return reverse_lazy('notesapp:post_detail', args=(self.object.id,))

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        # Если пользователь не является автором, отправляем его в свою библиотеку
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notesapp:notes_list'))
        return super().dispatch(*args, **kwargs)


class NoteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    template_name = 'notes/post_create.html'
    success_message = "Успешно добавленно"

    def get_form(self, form_class=NoteEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = f'Создать: '
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notesapp:notes_list')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NoteBasketListView(ListView):
    paginate_by = PAGINATE_BY_NOTES
    model = Note
    template_name = 'notes/posts_basket.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user, is_active=False)
        # return Note.objects.filter(category__pk=self.kwargs.get('pk')).order_by('-is_active')

    def get_context_data(self, **kwargs):
        context = super(NoteBasketListView, self).get_context_data(**kwargs)
        # context = Note.objects.filter(author=self.request.user)
        context['title_page'] = 'Корзина'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NoteBasketDelUpdateView(SuccessMessageMixin, UpdateView):
    model = Note
    context_object_name = 'post'
    template_name = 'notes/post_basket_add.html'
    success_message = "Успешно добавлено в корзину"

    def get_form(self, form_class=NoteBasketForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.is_active = False
        form.instance.is_favorites = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = f'Удалить: "{context.get(self, self.object.title)}"'
        context['pk'] = self.object.id
        context['name_button'] = 'Удалить'
        context['alert_text'] = 'Вы пытаетесь добавить заметку в корзину!'
        # author_pk = context.get(self, self.object.author.pk)
        # request_user_pk = self.request.user.pk
        return context

    def get_success_url(self):
        return reverse_lazy('notesapp:notes_list')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        # Если пользователь не является автором, отправляем его в свою библиотеку
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notesapp:notes_list'))
        return super().dispatch(*args, **kwargs)


class NoteBasketDetailView(DetailView):
    model = Note
    template_name = 'notes/post_basket_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.id
        context['title_page'] = f'{context.get(self, self.object.title)}'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notesapp:notes_list'))
        return super().dispatch(*args, **kwargs)


class NoteBasketDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Note
    context_object_name = 'post'
    template_name = 'notes/post_basket_delete.html'
    success_message = "Успешно удалено"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = f'Удалить: "{context.get(self, self.object.title)}"'
        return context

    def get_success_url(self):
        return reverse_lazy('notesapp:posts_basket_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message)
        success_url = self.get_success_url()
        obj.delete()
        return HttpResponseRedirect(success_url)

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notesapp:posts_basket_list'))
        return super().dispatch(*args, **kwargs)


class NoteReturnActiveUpdateView(SuccessMessageMixin, UpdateView):
    model = Note
    context_object_name = 'post'
    template_name = 'notes/post_basket_add.html'
    success_message = "Успешно восстановленно"

    def get_form(self, form_class=NoteReturnBasketForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.is_active = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = f'Восстановить заметку: "{context.get(self, self.object.title)}"'
        context['pk'] = self.object.id
        context['name_button'] = 'Восстановить'
        context['alert_text'] = 'Вы пытаетесь восстановить заметку.'

        # author_pk = context.get(self, self.object.author.pk)
        # request_user_pk = self.request.user.pk
        return context

    def get_success_url(self):
        return reverse_lazy('notesapp:posts_basket_list')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        # Если пользователь не является автором, отправляем его в свою библиотеку
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notesapp:posts_basket_list'))
        return super().dispatch(*args, **kwargs)


class NoteFavoriteListView(ListView):
    paginate_by = PAGINATE_BY_NOTES
    model = Note
    template_name = 'notes/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user, is_favorites=True).order_by('-is_favorites', '-created')
        # return Note.objects.filter(category__pk=self.kwargs.get('pk')).order_by('-is_active')

    def get_context_data(self, **kwargs):
        context = super(NoteFavoriteListView, self).get_context_data(**kwargs)
        # context = Note.objects.filter(author=self.request.user)
        context['title_page'] = 'Список избранных'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
