import random

from .models import Card

RARITY_CHANCES = {
    'common': 50,
    'rare': 25,
    'epic': 13,
    'legendary': 7,
    'secret': 5,
}

def draw_card():
    cards = list(Card.objects.all())

    if not cards:
        return None

    # Оставляем только те редкости, для которых есть карты
    available_rarities = []
    available_chances = []

    for rarity, chance in RARITY_CHANCES.items():
        if any(card.rarity == rarity for card in cards):
            available_rarities.append(rarity)
            available_chances.append(chance)

    if not available_rarities:
        return None

    # Сначала выбираем редкость
    chosen_rarity = random.choices(
        available_rarities,
        weights=available_chances,
        k=1
    )[0]

    # Потом случайную карту этой редкости
    rarity_cards = [
        card for card in cards
        if card.rarity == chosen_rarity
    ]

    return random.choice(rarity_cards)