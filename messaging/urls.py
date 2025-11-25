from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    path('profile-created/', views.profile_created, name='profile_created'),
    
    # Public profile
    path('u/<str:username>/', views.public_profile, name='public_profile'),
    path('u/<str:username>/send/', views.send_message_ajax, name='send_message_ajax'),
    
    # Dashboard
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('dashboard/<str:username>/auth/', views.dashboard_auth, name='dashboard_auth'),
    path('dashboard/<str:username>/logout/', views.logout_dashboard, name='logout_dashboard'),
    path('dashboard/<str:username>/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('dashboard/<str:username>/delete-all/', views.delete_all_messages, name='delete_all_messages'),
    path('dashboard/<str:username>/message-image/<int:message_id>/', views.generate_message_image, name='generate_message_image'),
]
