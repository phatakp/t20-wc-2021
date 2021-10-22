from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from .signals import match_receiver
        Match = self.get_model('Match')
        post_save.connect(match_receiver, sender=Match)
