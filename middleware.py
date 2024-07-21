import re
from django.http import HttpResponseForbidden
from configparser import ConfigParser

# Load patterns from config file and precompile regex patterns for performance
config = ConfigParser()
config.read('regex_patterns.ini')
# Load patterns from config file and precompile regex patterns for performance
compiled_patterns = {}
for section in config.sections():
    patterns_list = [config.get(section, option).replace("\\", "").replace("\n", "") for option in config.options(section)]
    compiled_patterns[section] = [re.compile(r"{pattern}", re.IGNORECASE) for pattern in patterns_list]

class SQLInjectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Intercept request, check for regex patterns in content, return response if no pattern matches
        for key, value in request.GET.items():
            for category, patterns in compiled_patterns.items():
                for pattern in patterns:
                    if pattern.search(value):
                        return HttpResponseForbidden(f"{category.replace("_", " ")} detected!")

        for key, value in request.POST.items():
            for category, pattern in compiled_patterns.items():
                if pattern.search(value):
                    return HttpResponseForbidden(f"{category.replace("_", " ")} detected!")

        response = self.get_response(request)
        return response
