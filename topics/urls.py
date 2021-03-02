from django.urls import path, include



from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.TopicsTop.as_view(), name='topics_top'),
    path('create_topic/', views.CreateTopicTop.as_view(), name='create_topic'),

    path('<str:name>/', views.SubjectView.as_view(), name='subject'),
    path('create_other_topic', views.noclassTopicFormView.as_view(), name='create_other_topic'),
]