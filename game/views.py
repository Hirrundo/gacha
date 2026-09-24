from django.shortcuts import render
from django.http import JsonResponse
from .models import Collection, Player,Character
from .gacha import draw_card

def draw(request):
    card = draw_card()

    if card is None:
        return JsonResponse({
            'error': 'Карты пока не добавлены'
        })

    player = Player.objects.first()

    if player is None:
        return JsonResponse({
            'error': 'Игроки пока не созданы'
        })

    collection, created = Collection.objects.get_or_create(
        player=player,
        card=card,
        defaults={'quantity': 1}
    )

    if not created:
        collection.quantity += 1
        collection.save()

    return JsonResponse({
        'id': card.id,
        'name': card.name,
        'rarity': card.rarity,
        'description': card.description,
        'quantity': collection.quantity,
    })
def draw_page(request):
    return render(request, 'game/draw.html')
def home(request):
    characters = Character.objects.all()

    return render(
        request,
        'game/home.html',
        {'characters': characters}
    )

# Create your views here.
