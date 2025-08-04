from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('delete_topic/<uuid:topic_id>/', views.delete_topic, name='delete_topic'),
]