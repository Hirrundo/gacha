from django.db import models

from django.db import models

class Card(models.Model):
    RARITY_CHOICES = [
        ('common', 'Обычная'),
        ('rare', 'Редкая'),
        ('epic', 'Эпическая'),
        ('legendary', 'Легендарная'),
        ('secret', 'Секретная'),
    ]

    name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=50, choices=RARITY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='cards/')
    drop_chance = models.FloatField()

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    username = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(
    upload_to='avatars/',
    null=True,
    blank=True
)
    hearts = models.PositiveIntegerField(default=0)
    spins = models.PositiveIntegerField(default=0)
    welcome_bonus_received = models.BooleanField(default=False)
    characters = models.ManyToManyField(
    'Character',
    blank=True
)

    def __str__(self):
        return self.username

class Collection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('player', 'card')

    def __str__(self):
        return f'{self.player} — {self.card}'

class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='characters/')

    def __str__(self):
        return self.name

class InteractionCooldown(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    action_1_at = models.DateTimeField(null=True, blank=True)
    action_2_at = models.DateTimeField(null=True, blank=True)
    action_3_at = models.DateTimeField(null=True, blank=True)
    action_4_at = models.DateTimeField(null=True, blank=True)
    action_5_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('player', 'character')

class InteractionScene(models.Model):
    ACTION_CHOICES = [
        (1, 'Действие 1'),
        (2, 'Действие 2'),
        (3, 'Действие 3'),
        (4, 'Действие 4'),
        (5, 'Действие 5'),
    ]

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)

    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to='interactions/')

    def __str__(self):
        return f'{self.character} — действие {self.action} — {self.title}'


# Create your models here.
