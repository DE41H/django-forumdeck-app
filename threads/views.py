from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from threads.models import *
from threads.forms import *

# Create your views here.

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(generic.ListView):
    model = Thread
    template_name = 'forum/category_detail.html'
    context_object_name = 'threads'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Thread.objects.filter(category=self.category).order_by('-created_at')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ReportCreateView(generic.CreateView):
    model = Report
    form_class = ReportCreateForm
    template_name = 'forum/report_form.html'
    success_url = reverse_lazy('threads:category_list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.reporter = self.request.user
        form.instance.reported_type = self.kwargs['object_type']
        form.instance.reported_pk = self.kwargs['object_pk']
        return super().form_valid(form)
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object_type = self.kwargs.get('object_type')
        self.object_pk = self.kwargs.get('object_pk')
        if self.object_type not in ('thread', 'reply'):
            raise Http404('Invalid content type')
        if self.object_type == 'thread':
            self.object = get_object_or_404(Thread, pk=self.object_pk)
        elif self.object_type == 'reply':
            self.object = get_object_or_404(Reply, pk=self.object_pk)
        return super().dispatch(request, *args, **kwargs)
