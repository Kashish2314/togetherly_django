from django.apps import AppConfig


class ChallengesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'challenges'
    verbose_name = 'Challenges'

    def ready(self):
        import challenges.models  # Import signals
