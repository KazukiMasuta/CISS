from django.urls import path, include

from cissapp.views import DetailView, IndexView, upload, TopicDetailView,FirstView

from . import views

app_name = 'cissapp'

urlpatterns = [
    path('', FirstView.as_view(), name='first'),
    path('cissapp/', IndexView.as_view(), name='index'),

    path('search', views.search, name='search'),
    path('<int:pk>/', views.TopicDetailView.as_view(), name='detail'),
    path('upload/', views.upload, name='upload'),
]