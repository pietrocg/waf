import re
from django.db import connection
from configparser import ConfigParser

# Load patterns from config file and precompile regex patterns for performance
config = ConfigParser()
config.read('regex_patterns.ini')
compiled_patterns = {}
for section in config.sections():
    # This is ugly, must find nicer way to clean the text
    patterns_list = [config.get(section, option).replace("\\", "").replace("\n", "") for option in config.options(section)]
    compiled_patterns[section] = [re.compile(r"{pattern}", re.IGNORECASE) for pattern in patterns_list]
original_execute = connection.cursor().execute

def execute_wrapper(sql, params=None):
    # Check for regex patterns in SQL queries
    for category, patterns in compiled_patterns.items():
        for pattern in patterns:
            if pattern.search(sql):
                raise Exception(f"{category.replace("_", " ")} detected!")
    return original_execute(sql, params)

# monkey patch execute method
connection.cursor().execute = execute_wrapper
