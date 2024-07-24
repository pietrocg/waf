## WAF PoC

# Install
You can install the package with '''pip install waf''' and use the package with '''import waf'''. 
The package adds itself to the Django projects Middleware and apps.

# How does it work?
This WAF PoC contains 3 separate injection detection mechanisms:

- The SQL wrapper function, that monkey patches the original Django.db connection function and the SQL compiler, checking against malicious patterns. This will detect any attempts to manipulate SQl functions through the database connection strings. The code for this is in 'db_query_wrapper.py'.

- The SQL injection middleware, that intercepts incoming ad outgoing requests, and checks for strings that can be used for injection. You can find the code for this in 'middleware.py'.

- The rate limiting middleware limits each user to 1000 requests per minute, on a running base. 
