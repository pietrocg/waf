from collections import defaultdict, deque
from time import time
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_requests = defaultdict(lambda: deque(maxlen=1000))  # Limit to 1000 requests

    def __call__(self, request):
        user_id = request.META.get('REMOTE_ADDR')  # Should probably implement something more accurate, like maybe looking at request metadata, user agent, or provided user ID
        current_time = time()
        
        self.user_requests[user_id].append(current_time)
        # Remove requests older than 60 seconds
        while self.user_requests[user_id] and current_time - self.user_requests[user_id][0] > 60:
            self.user_requests[user_id].popleft()

        if len(self.user_requests[user_id]) >= 1000:
            return HttpResponseForbidden("Rate limit exceeded!")

        response = self.get_response(request)
        return response
