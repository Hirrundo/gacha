from django.contrib import admin
from .models import Card,Player,Collection,Character,InteractionScene

admin.site.register(Card)
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    filter_horizontal = ('characters',)
admin.site.register(Collection)
admin.site.register(Character)
admin.site.register(InteractionScene)

# Register your models here.
