from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ cookiecutter.project_slug }}.common"
    verbose_name = "Common"

    def ready(self):
        try:
            import {{ cookiecutter.project_slug }}.common.signals  # noqa: F401
        except ImportError:
            pass
