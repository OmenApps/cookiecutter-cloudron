from datetime import datetime
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.db import connection
{% if cookiecutter.use_redis == "yes" %}from django_redis import get_redis_connection{% endif %}
from ninja import Router

from . import api
from .schemas import DetailedHealthSchema, HealthSchema

router = Router(tags=["Health"])


@router.get("/health", response=HealthSchema, auth=None)
def health_check(request) -> dict[str, Any]:
    """
    Basic health check endpoint
    """
    return {"status": "healthy", "version": settings.VERSION, "timestamp": datetime.now()}


@router.get("/health/detailed", response=DetailedHealthSchema)
def detailed_health_check(request) -> dict[str, Any]:
    """
    Detailed health check for authenticated users
    """
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            database_healthy = True
    except Exception:
        database_healthy = False

    # Check cache
    try:
        cache.set("health_check", "ok", 1)
        cache_healthy = cache.get("health_check") == "ok"
    except Exception:
        cache_healthy = False

    {% if cookiecutter.use_redis == "yes" %}
    # Check Redis
    try:
        redis_client = get_redis_connection("default")
        redis_healthy = redis_client.ping()
    except Exception:
        redis_healthy = False
    {% endif %}

    # Check storage
    storage_healthy = True  # Add your storage check logic here

    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.now(),
        "database": database_healthy,
        "cache": cache_healthy,
        {% if cookiecutter.use_redis == "yes" %}"redis": redis_healthy,{% endif %}
        "storage": storage_healthy,
    }


api.add_router("/", router)
