from django.urls import path
from . import views

urlpatterns = [
    path('', views.heroes, name='heroes'),
    path('post_hero/', views.post_hero, name='post_hero'),
    path('<slug:slug>/', views.biography, name='biography'),
    path('update/<slug:slug>/', views.update_hero, name='update_hero'),
    path('delete/<slug:slug>/', views.delete_hero, name='delete_hero'),
    path('<int:comment_id>/like/', views.comment_like, name='comment_like'),
]
