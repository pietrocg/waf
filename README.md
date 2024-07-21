# WAF PoC

When the package is uploaded to the Python repository, you should be able to install the package with 'pip install waf' and use the package with 'import waf'. The package should work off the bat as in the initialization it adds itself to the Django projects Middleware and apps.

The SQL wrapper function will automatically overwrite the execute function by monkey patching it, but I also monkey patched the Django ORM SQL function to demonstrate two different approaches. 