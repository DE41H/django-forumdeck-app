from django.urls import path
from threads.views import *

app_name = 'threads'
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:category_slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('reports/<str:object_type>/<int:object_pk>', ReportCreateView.as_view(), name='report')
]
