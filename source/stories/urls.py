from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    path('diziler/', views.category_page, {'category': 'series'}, name='diziler'),
    path('filmler/', views.category_page, {'category': 'movie'}, name='filmler'),
    path('animasyon/', views.category_page, {'category': 'animation'}, name='animasyon'),
    path('oyunlar/', views.category_page, {'category': 'game'}, name='oyunlar'),
    path('sozluk/', views.sozluk, name='sozluk'),
    path('api/fetch-word/', views.fetch_word_api, name='fetch_word_api'),
]
