import logging

from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)


@never_cache
@require_GET
def profile_view(request):
    """View for the user's profile page."""
    logger.info("Profile view accessed.")
    return JsonResponse({"name": request.user.name, "email": request.user.email})
