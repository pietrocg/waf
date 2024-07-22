import waf.source.db_query_wrapper
import waf.source.middleware
import waf.source.rate_limit_middleware
from django.db.models.sql.compiler import SQLCompiler
from django.conf import settings

# this import assumes a very specific structure of the project

default_app_config = 'engine.apps.EngineConfig'

# This monkey patches execute_sql method of SQLCompiler, so directly on ORM queries

original_execute_sql = SQLCompiler.execute_sql

def wrapped_execute_sql(self, *args, **kwargs):
    query = str(self.query)
    waf.source.db_query_wrapper.execute_wrapper(query)
    return original_execute_sql(self, *args, **kwargs)

SQLCompiler.execute_sql = wrapped_execute_sql

def initialize_firewall():
    # Patching ORM execute_sql method
    SQLCompiler.execute_sql = wrapped_execute_sql

# Adding the middleware to the settings so that it is a 1 line install
def auto_configure_django():
    # Adding middleware to settings
    if 'waf.source.middleware.SQLInjectionMiddleware' not in settings.MIDDLEWARE:
        settings.MIDDLEWARE.append('waf.source.middleware.SQLInjectionMiddleware')
    
    #  Adding rate limit middleware
    if 'waf.rate_limit_middleware.RateLimitMiddleware' not in settings.MIDDLEWARE:
        settings.MIDDLEWARE.append('waf.source.rate_limit_middleware.RateLimitMiddleware')
    
    # Adding waf app to INSTALLED_APPS - really need to work on my naming
    if 'waf' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS.append('waf')

initialize_firewall()
auto_configure_django()