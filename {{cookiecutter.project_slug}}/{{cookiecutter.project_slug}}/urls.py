"""URL Configuration for {{ cookiecutter.project_slug }}."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from {{ cookiecutter.project_slug }}.common.views import health_check_view, health_check_full
from {{ cookiecutter.project_slug }}.api import api


# Django Admin customization
admin.site.site_header = "{{ cookiecutter.project_name }} Admin"
admin.site.site_title = "{{ cookiecutter.project_name }} Admin Portal"
admin.site.index_title = "Welcome to {{ cookiecutter.project_name }} Admin Portal"

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    
    # Health Check Endpoints
    path("health/", health_check_view, name="health-check-simple"),
    path("health/full/", health_check_full, name="health-check-full"),
    
    # API URLs
    path("api/", api.urls),
    
    # Authentication URLs (django-allauth)
    path("accounts/", include("allauth.urls")),
    path("accounts/mfa/", include("allauth.mfa.urls")),
    
    # Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls")),
    
    # Your app URLs
    path("", include("{{ cookiecutter.project_slug }}.common.urls")),
    path("users/", include("{{ cookiecutter.project_slug }}.users.urls")),
]

# Static/Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add simple health check endpoint for container health checks
# This is in addition to the more comprehensive django-health-check endpoints
urlpatterns += [
    path("ping/", health_check_view, name="ping"),
]

handler400 = "{{ cookiecutter.project_slug }}.common.views.bad_request"
handler403 = "{{ cookiecutter.project_slug }}.common.views.permission_denied"
handler404 = "{{ cookiecutter.project_slug }}.common.views.page_not_found"
handler500 = "{{ cookiecutter.project_slug }}.common.views.server_error"