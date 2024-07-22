from django.apps import AppConfig


class EngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'waf'
    def ready(self):
        # Ensure db_wrapper is loaded to patch the database execute method
        import waf.db_query_wrapper
        import waf.middleware
        import waf.rate_limit_middleware
