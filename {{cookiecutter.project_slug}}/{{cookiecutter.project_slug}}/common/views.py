import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from health_check.views import MainView

logger = logging.getLogger(__name__)


@never_cache
@require_GET
def health_check_view(request):
    """Custom health check view that returns a simple JSON response.

    For more detailed health checks, use the django-health-check views.
    """
    logger.info("Health check accessed.")
    return JsonResponse({"status": "ok"})


# Use MainView from django-health-check for detailed checks
health_check_full = never_cache(MainView.as_view())


def home_view(request):
    """Home view for the site."""
    logger.info("Home view accessed.")

    return render(request, "base.html")


def bad_request(request, exception):
    """Custom 400 error handler."""
    return render(request, "400.html", status=400)


def permission_denied(request, exception):
    """Custom 403 error handler."""
    return render(request, "403.html", status=403)


def page_not_found(request, exception):
    """Custom 404 error handler."""
    return render(request, "404.html", status=404)


def server_error(request):
    """Custom 500 error handler."""
    return render(request, "500.html", status=500)
