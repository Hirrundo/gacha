from django.db import models

class Card (models.Model):
    RARITY_CHOICES = [
        ('common', 'Обычная'),
        ('rare', 'Редкая'),
        ('epic', 'Эпическая'),
        ('legendary', 'Легендарная'),
        ('secret', 'Секретная'),
    ]
    
    name=models.CharField(max_length=100)
    rarity=models.CharField(max_length=50,choices=RARITY_CHOICES)
    description=models.TextField()
    image=models.ImageField(upload_to='cards/')
    drop_chance = models.FloatField()

    def __str__(self):
        return self.name

class Player(models.Model):
    username = models.CharField(max_length=50, unique=True)

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
    


# Create your models here.
