from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from .models import Student

class StudentAccessMiddleware(MiddlewareMixin):
    """
    Redirects authenticated student users to the tutorials section
    if they try to access any page outside the allowed prefixes.
    """
    def process_request(self, request):
        # Only apply to authenticated users with a linked Student record
        if request.user.is_authenticated and Student.objects.filter(user=request.user).exists():
            # Allowed path prefixes for students
            allowed_prefixes = [
                '/tutorials/',      # main tutorials area
                '/logout/',          # logout
                '/static/',          # static files (CSS, JS)
                '/media/',           # uploaded files
            ]
            path = request.path_info
            # Allow if the current path starts with any allowed prefix
            if any(path.startswith(prefix) for prefix in allowed_prefixes):
                return None
            # Otherwise, redirect to the tutorial list
            return redirect('tutorial_list')
        return None