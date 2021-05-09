from django.urls import path, include



from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.TopicsTop.as_view(), name='topics_top'),
    path('<int:pk>/', views.TopicDetailView.as_view(), name='detail'),
    path('create_other_topic', views.noclassTopicFormView.as_view(), name='create_other_topic'),
]