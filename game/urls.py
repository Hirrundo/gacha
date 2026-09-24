from django.urls import path

from .views import draw, draw_page,home

urlpatterns = [
    path('', home, name='home'),
    path('gacha/', draw_page, name='gacha'),
    path('draw/', draw, name='draw'),

]