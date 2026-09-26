import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Collection, Player,Character,InteractionCooldown,InteractionScene
from .gacha import draw_card

def draw(request):
    card = draw_card()

    if card is None:
        return JsonResponse({
            'error': 'Карты пока не добавлены'
        })

    player = Player.objects.get(user=request.user)

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

    player = None
    welcome_bonus = request.session.pop('welcome_bonus', False)

    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)

    return render(
        request,
        'game/home.html',
        {
            'characters': characters,
            'player': player,
            'welcome_bonus': welcome_bonus,
        }
    )
def character_detail(request, character_id):
    character = Character.objects.get(id=character_id)

    player = None

    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)

    return render(
        request,
        'game/character_detail.html',
        {
            'character': character,
            'player': player,
        }
    )
def interaction(request, character_id, action):
    if not request.user.is_authenticated:

        messages = [
            'Сначала войди, а потом уже трогай мужиков.',
            'Анонимус, тебе сюда пока нельзя 👁️',
            'Логин забыл, а персонажа уже выбрал.',
            'Сначала аккаунт, потом романтика.',
            'Ты кто вообще такой? Авторизуйся.',
        ]

        return JsonResponse({
            'error': random.choice(messages)
        }, status=401)

    player = Player.objects.get(user=request.user)

    if player is None:
        return JsonResponse({'error': 'Игрок не найден'})

    character = Character.objects.get(id=character_id)

    if not player.characters.filter(id=character_id).exists():

        messages = [
            'Эй, руки убрал. Это не твой мужик.',
            'Доступ запрещён. Собственник уже выехал.',
            'Ты вообще-то не в своём разделе, дружочек.',
            'Этот экземпляр уже занят. Иди ищи своего.',
            'Попытка увести чужого мужика зафиксирована 👁️',
        ]

        return JsonResponse({
            'error': random.choice(messages)
        }, status=403)

    cooldown, created = InteractionCooldown.objects.get_or_create(
        player=player,
        character=character
    )

    now = timezone.now()

    settings = {
        1: {
            'cooldown': timedelta(minutes=2),
            'reward': 1,
            'field': 'action_1_at',
        },
        2: {
            'cooldown': timedelta(minutes=5),
            'reward': 3,
            'field': 'action_2_at',
        },
        3: {
            'cooldown': timedelta(minutes=7),
            'reward': 10,
            'field': 'action_3_at',
        },
        4: {
            'cooldown': timedelta(minutes=15),
            'reward': 15,
            'field': 'action_4_at',
        },
        5: {
            'cooldown': timedelta(minutes=30),
            'reward': 25,
            'field': 'action_5_at',
        },
    }

    if action not in settings:
        return JsonResponse({'error': 'Такого действия нет'})

    current = getattr(cooldown, settings[action]['field'])

    if current is not None:
        if now < current + settings[action]['cooldown']:
            remaining = (
                current
                + settings[action]['cooldown']
                - now
            ).total_seconds()

            return JsonResponse({
                'error': 'Действие пока недоступно',
                'remaining': int(remaining),
            })

    reward = settings[action]['reward']

    scenes = InteractionScene.objects.filter(
        character=character,
        action=action
    )

    if not scenes.exists():
        return JsonResponse({
            'error': 'Для этого действия пока нет сценок'
        })

    scene = random.choice(list(scenes))

    player.hearts += reward
    player.save()

    setattr(cooldown, settings[action]['field'], now)
    cooldown.save()

    return JsonResponse({
        'success': True,
        'reward': reward,
        'hearts': player.hearts,
        'title': scene.title,
        'text': scene.text,
        'image': scene.image.url,
    })
def interaction_status(request, character_id):
    player = Player.objects.get(user=request.user)

    if player is None:
        return JsonResponse({'error': 'Игрок не найден'})

    character = Character.objects.get(id=character_id)

    cooldown, created = InteractionCooldown.objects.get_or_create(
        player=player,
        character=character
    )

    now = timezone.now()

    settings = {
        1: timedelta(minutes=2),
        2: timedelta(minutes=5),
        3: timedelta(minutes=7),
        4: timedelta(minutes=15),
        5: timedelta(minutes=30),
    }

    result = {}

    for action in range(1, 6):
        field = f'action_{action}_at'
        current = getattr(cooldown, field)

        if current is None:
            result[action] = 0
            continue

        remaining = (
            current + settings[action] - now
        ).total_seconds()

        result[action] = max(0, int(remaining))

    return JsonResponse({
        'cooldowns': result
    })
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            player = Player.objects.get(user=user)

            if not player.welcome_bonus_received:
                player.hearts += 10
                player.spins += 10
                player.welcome_bonus_received = True
                player.save()

                request.session['welcome_bonus'] = True

            return redirect('home')
        return render(
            request,
            'game/login.html',
            {'error': 'Неверный логин или пароль'}
        )

    return render(request, 'game/login.html')
def logout_page(request):
    logout(request)
    return redirect('home')
def profile(request):
    player = Player.objects.get(user=request.user)

    collection = Collection.objects.filter(
        player=player
    ).select_related('card')
    characters = player.characters.all()
    return render(
        request,
        'game/profile.html',
        {
            'player': player,
            'collection': collection,
            'characters': characters,
        }
    )
def edit_profile(request):
    player = Player.objects.get(user=request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        avatar = request.FILES.get('avatar')

        if username:
            player.username = username

        if avatar:
            player.avatar = avatar

        player.save()

        return redirect('profile')

    return render(
        request,
        'game/edit_profile.html',
        {
            'player': player,
        }
    )
@csrf_exempt
def exchange_hearts(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Сначала войди в аккаунт.'
        }, status=401)

    player = Player.objects.get(user=request.user)

    amount = int(request.POST.get('amount', 0))

    exchange_rates = {
        5: 1,
        25: 10,
    }

    if amount not in exchange_rates:
        return JsonResponse({
            'error': 'Такого обмена нет.'
        }, status=400)

    if player.hearts < amount:
        return JsonResponse({
            'error': 'Недостаточно сердец.'
        }, status=400)

    player.hearts -= amount
    player.spins += exchange_rates[amount]
    player.save()

    return JsonResponse({
        'success': True,
        'hearts': player.hearts,
        'spins': player.spins,
    })
# Create your views here.
