from django.urls import path
from threads.views import *

app_name = 'threads'
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/<str:order_by>/', ThreadListView.as_view(), name='thread_list'),
    path('thread/<int:pk>/<str:order_by>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/create/<int:pk>/', ThreadCreateView.as_view(), name='thread_create'),
    path('thread/report/<int:pk>/<str:type>/', ReportCreateView.as_view(), name='report_create'),
    path('thread/upvote/<int:pk>/<str:type>/', UpvoteView.as_view(), name='upvote')
]
