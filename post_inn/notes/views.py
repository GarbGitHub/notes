from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from notes.forms import NoteEditForm
from notes.models import Note
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class NoteListView(ListView):
    paginate_by = 5
    model = Note
    template_name = 'notes/posts.html'
    context_object_name = 'objects'
    ordering = '-created'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
        # return Note.objects.filter(category__pk=self.kwargs.get('pk')).order_by('-is_active')

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        # context = Note.objects.filter(author=self.request.user)
        title_page = 'List of notes'
        context['title_page'] = title_page
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
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notes_list'))
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
        return reverse_lazy('post_detail', args=(self.object.id,))

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        # Если пользователь не является автором, отправляем его в свою библиотеку
        if obj.author.pk != self.request.user.pk:
            return HttpResponseRedirect(reverse('notes_list'))
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
        return reverse_lazy('notes_list')

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NoteDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Note
    context_object_name = 'post'
    template_name = 'notes/post_delete.html'
    success_message = "Успешно удалено"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = f'Удалить: "{context.get(self, self.object.title)}"'
        return context

    def get_success_url(self):
        return reverse_lazy('notes_list')

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
            return HttpResponseRedirect(reverse('notes_list'))
        return super().dispatch(*args, **kwargs)
