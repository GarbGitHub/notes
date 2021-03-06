import logging
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from notes.forms import NoteBasketForm, NoteReturnBasketForm, NoteUpdateForm, NoteCreateForm, TagCreateForm, \
    TagUpdateForm
from notes.models import Note, Tag
from post_inn import get_config
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

PAGINATE_BY_NOTES = 10


def index(request):
    context = {
        'title_page': 'Заметочник - ваши заметки всегда с вами',
        'description': 'Заметочник - это простой способ создавать и сохранять ваши заметки. Получите доступ к вашим заметкам с любых устройств.',
        'static_get_param': get_config.GET_CONFIG
    }

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('notesapp:notes_list'))
    return render(request, 'accounts/register_base.html', context)


class SearchResultsView(ListView):
    paginate_by = PAGINATE_BY_NOTES
    model = Note
    template_name = 'notes/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if len(query) == 0:
            return []
        objects = Note.objects.filter(Q(title__icontains=query) | Q(text__icontains=query),
                                      author=self.request.user,
                                      is_active=True)
        part = list(objects.filter(title__icontains=query)) + list(objects.filter(text__icontains=query))
        return part

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)

        context['title_page'] = 'Поиск'
        context['static_get_param'] = get_config.GET_CONFIG

        if len(self.request.GET.get('q')) == 0:
            context['no_search_result'] = 'Задан пустой запрос'

        elif not self.get_queryset():
            context['no_search_result'] = 'Ничего не найдено'

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
        context['title_page'] = 'Заметки'
        context['static_get_param'] = get_config.GET_CONFIG
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NoteTagListView(ListView):
    paginate_by = PAGINATE_BY_NOTES
    model = Note
    template_name = 'notes/posts.html'
    context_object_name = 'posts'
    ordering = '-created'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user, is_active=True, tags=self.kwargs['pk']).order_by(
            '-is_favorites', '-created')

    def get_context_data(self, **kwargs):
        context = super(NoteTagListView, self).get_context_data(**kwargs)
        context['title_page'] = 'Заметки'
        context['static_get_param'] = get_config.GET_CONFIG
        context['tags_pk'] = str(self.kwargs['pk'])
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        """Если пользователь не является автором коллекции, то перенаправляем его в свой список заметок"""
        tag_pk = self.kwargs['pk']
        author_pk = Tag.get_author_tag(request=self.request, tag_pk=tag_pk)
        if author_pk is None:
            return HttpResponseRedirect(reverse('notesapp:notes_list'))
        return super().dispatch(*args, **kwargs)


class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.id
        context['title_page'] = 'Заметки'
        context['static_get_param'] = get_config.GET_CONFIG
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

    def get_form(self, form_class=NoteUpdateForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super(NoteUpdateView, self).get_form_kwargs()
        kwargs['initial'].update({'user_pk': self.request.user.pk})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Править'
        # author_pk = context.get(self, self.object.author.pk)
        # request_user_pk = self.request.user.pk
        context['static_get_param'] = get_config.GET_CONFIG
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

    def get_form(self, form_class=NoteCreateForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super(NoteCreateView, self).get_form_kwargs()
        kwargs['initial'].update({'user_pk': self.request.user.pk})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Создать'
        context['static_get_param'] = get_config.GET_CONFIG
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

    def get_context_data(self, **kwargs):
        context = super(NoteBasketListView, self).get_context_data(**kwargs)
        context['title_page'] = 'Корзина'
        context['static_get_param'] = get_config.GET_CONFIG
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
        context['title_page'] = 'В Корзину'
        context['pk'] = self.object.id
        context['static_get_param'] = get_config.GET_CONFIG
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
        context['title_page'] = 'Корзина'
        context['static_get_param'] = get_config.GET_CONFIG
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
        context['title_page'] = 'Удалить'
        context['static_get_param'] = get_config.GET_CONFIG
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
    template_name = 'notes/return_note.html'
    success_message = "Успешно восстановлено"

    def get_form(self, form_class=NoteReturnBasketForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.is_active = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = f'Восстановить'
        context['pk'] = self.object.id
        context['static_get_param'] = get_config.GET_CONFIG
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
        context['title_page'] = 'Избранное'
        context['static_get_param'] = get_config.GET_CONFIG
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def offline(request):
    return render(request, 'notes/offline.html')


class TagsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    template_name = 'notes/tag_create.html'
    success_message = "Успешно добавлено"

    def get_form(self, form_class=TagCreateForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Теги'
        context['static_get_param'] = get_config.GET_CONFIG
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notesapp:tags')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TagsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'notes/tag_delete.html'
    success_message = "Тег удален"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Удалить'
        context['static_get_param'] = get_config.GET_CONFIG
        return context

    def get_success_url(self):
        return reverse_lazy('notesapp:tags')

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
            return HttpResponseRedirect(reverse('notesapp:tags'))
        return super().dispatch(*args, **kwargs)


class TagUpdateView(SuccessMessageMixin, UpdateView):
    model = Tag
    template_name = 'notes/tag_update.html'
    success_message = "Тег отредактирован"

    def get_form(self, form_class=TagUpdateForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super(TagUpdateView, self).get_form_kwargs()
        kwargs['initial'].update({'user_pk': self.request.user.pk})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Править тег'
        context['static_get_param'] = get_config.GET_CONFIG
        return context

    def get_success_url(self):
        return reverse_lazy('notesapp:tags')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        # Если пользователь не является автором, отправляем его в свою библиотеку
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notesapp:tags'))
        return super().dispatch(*args, **kwargs)
