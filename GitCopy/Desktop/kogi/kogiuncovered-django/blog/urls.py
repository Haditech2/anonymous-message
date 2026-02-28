from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.articles_list, name='articles_list'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete-post/<slug:slug>/', views.delete_post, name='delete_post'),
    path('like/<slug:slug>/', views.toggle_like, name='toggle_like'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_of_service, name='terms'),
]
