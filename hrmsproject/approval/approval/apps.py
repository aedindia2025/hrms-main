from django.apps import AppConfig


class ApprovalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'approval.approval'  # Python import path
    label = 'approval'  # Database app label (for migrations)
