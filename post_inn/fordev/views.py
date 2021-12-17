from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from fordev.models import Page


class ForDevListView(ListView):
    paginate_by = 10
    model = Page
    template_name = 'notes/posts.html'
    context_object_name = 'posts'
    ordering = '-created'

    def get_queryset(self):
        return Page.objects.filter(is_active=True, category=1).order_by('-is_boxed', '-created')

    def get_context_data(self, **kwargs):
        context = super(ForDevListView, self).get_context_data(**kwargs)
        context['title_page'] = 'Разработчику'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ForDevDetailView(DetailView):
    model = Page
    template_name = 'notes/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.id
        # context['title_page'] = f'{context.get(self, self.object.title)}'
        context['title_page'] = 'API'
        context['cat_pk'] = f'Категория: "{context.get(self, self.object.category.pk)}"'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='auth:login'))
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        return super().dispatch(*args, **kwargs)
