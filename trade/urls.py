from django.urls import path

from . import views
app_name = 'trade'

urlpatterns = [
    path('', views.TradeTopicView.as_view(), name='top'),
    path('create_topic/', views.TopicCreateView.as_view(), name='create_topic'),
    path('<int:pk>/', views.TopicAndCommentView.as_view(), name='topic'),
]