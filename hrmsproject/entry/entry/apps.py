from django.apps import AppConfig


class EntryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entry.entry'  # Python import path
    label = 'entry'  # Database app label (for migrations)
