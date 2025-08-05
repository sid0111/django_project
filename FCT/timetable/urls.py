# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/topics/', views.get_topics, name='get_topics'), # New line
    path('add_topic/', views.add_topic, name='add_topic'),
    path('delete_topic/<uuid:topic_id>/', views.delete_topic, name='delete_topic'),
]