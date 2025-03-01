from django.urls import path

from {{ cookiecutter.project_slug }}.common.views import (
    bad_request,
    health_check_view,
    page_not_found,
    permission_denied,
    server_error,
)

app_name = "common"

urlpatterns = [
    path("health_check/", health_check_view, name="health_check"),
    path("400/", bad_request, name="bad_request"),
    path("403/", permission_denied, name="permission_denied"),
    path("404/", page_not_found, name="page_not_found"),
    path("500/", server_error, name="server_error"),
]
