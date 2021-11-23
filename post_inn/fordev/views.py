from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from fordev.models import Page


class FordevListView(ListView):
    paginate_by = 5
    model = Page
    template_name = 'fordev/list_pages.html'
    context_object_name = 'objects'
    ordering = '-created'

    def get_queryset(self):
        return Page.objects.filter(is_active=True).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(FordevListView, self).get_context_data(**kwargs)
        context['title_page'] = 'Список заметок'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FordevDetailView(DetailView):
    model = Page
    template_name = 'fordev/page.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.id
        context['title_page'] = f'{context.get(self, self.object.title)}'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        return super().dispatch(*args, **kwargs)
