from django.views.generic import ListView, DetailView
from fordev.models import Page


class ForPageListView(ListView):
    paginate_by = 30
    model = Page
    template_name = 'fordev/list-pages.html'
    context_object_name = 'posts'
    ordering = '-created'

    def get_queryset(self):
        return Page.objects.filter(is_active=True, category=2).order_by('-is_boxed', '-created')

    def get_context_data(self, **kwargs):
        context = super(ForPageListView, self).get_context_data(**kwargs)
        context['title_page'] = 'Пользовательское соглашение'
        return context


class ForDevListView(ListView):
    paginate_by = 30
    model = Page
    template_name = 'fordev/index.html'
    context_object_name = 'posts'
    ordering = '-created'

    def get_queryset(self):
        return Page.objects.filter(is_active=True, category=1).order_by('-is_boxed', '-created')

    def get_context_data(self, **kwargs):
        context = super(ForDevListView, self).get_context_data(**kwargs)
        context['title_page'] = 'Разработчику'
        return context


class ForDevDetailView(DetailView):
    model = Page
    template_name = 'fordev/iner-page.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.id
        context['cat_pk'] = f'{context.get(self, self.object.category.name)}'
        return context

