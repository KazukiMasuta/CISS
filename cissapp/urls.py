from django.urls import path, include

from cissapp.views import DetailView, IndexView, upload, TopicDetailView

from . import views

app_name = 'cissapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', views.search, name='search'),
    #path('upload/', views.upload, name='upload'),
]