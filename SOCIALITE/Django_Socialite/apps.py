from django.apps import AppConfig


class DjangoSocialiteConfig(AppConfig):
    name = 'Django_Socialite'

    def ready(self):
        import Django_Socialite.signals
