from django.urls import path

from django.views.generic import TemplateView
from {{ cookiecutter.project_slug }}.common.views import (
    bad_request,
    health_check_view,
    health_check_full,
    home_view,
    page_not_found,
    permission_denied,
    server_error,
)

app_name = "common"

urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html"), name="home"),
    path("health/", health_check_view, name="health_check"),
    path("health/full/", health_check_full, name="health_check_full"),
    path("400/", bad_request, name="bad_request"),
    path("403/", permission_denied, name="permission_denied"),
    path("404/", page_not_found, name="page_not_found"),
    path("500/", server_error, name="server_error"),
]
