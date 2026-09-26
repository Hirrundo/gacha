from django.urls import path

from .views import draw, draw_page, exchange_hearts,home,character_detail,interaction,interaction_status,login_page, logout_page, profile,edit_profile

urlpatterns = [
    path('', home, name='home'),
    path('gacha/', draw_page, name='gacha'),
    path('draw/', draw, name='draw'),
    path('character/<int:character_id>',character_detail,name='character_detail'),
  path(
    'character/<int:character_id>/interaction/<int:action>/',
    interaction,
    name='interaction'),
    path('character/<int:character_id>/interaction-status/',
    interaction_status,
    name='interaction_status'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('exchange/', exchange_hearts, name='exchange_hearts'),
]