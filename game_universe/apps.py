from email.policy import default
from symtable import Class

from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game_universe'

    def ready(self):
        from . import signals
