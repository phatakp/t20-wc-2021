from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .signals import user_bet_receiver
        CustomUser = self.get_model('CustomUser')
        post_save.connect(user_bet_receiver, sender=CustomUser)
