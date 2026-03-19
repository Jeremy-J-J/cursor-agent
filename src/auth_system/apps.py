from django.apps import AppConfig


class AuthSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_system'
    
    def ready(self):
        # Import signals to ensure they're registered
        import auth_system.signals