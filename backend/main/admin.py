from django.contrib import admin
from .models import User, Word, Game, GuessedLetter


admin.site.register(User)
admin.site.register(Word)
admin.site.register(Game)
admin.site.register(GuessedLetter)
