from django.urls import path
from . import views

urlpatterns = [
    # Main app views
    path('index/', views.index, name='index'),
    path('api/topics/', views.get_topics, name='get_topics'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('delete_topic/<uuid:topic_id>/', views.delete_topic, name='delete_topic'),

    # Authentication views
    path('register/', views.register_view, name='register'),
    path('', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    # New user profile and settings views
    path('profile/', views.profile_and_password_change, name='profile_and_password_change'),
    path('settings/', views.settings_view, name='settings'),
]