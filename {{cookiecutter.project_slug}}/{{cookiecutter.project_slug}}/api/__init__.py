# {{ cookiecutter.project_slug }}/api/__init__.py
{% if cookiecutter.use_cloudron_auth == "yes" %}from allauth.socialaccount.models import SocialToken{% endif %}
from ninja import NinjaAPI, Redoc
from ninja.security import APIKeyHeader, HttpBearer


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        # Add your API key validation logic here
        # For example, check against a database of valid API keys
        if key == "secret":  # Change this to your actual validation
            return key
        return None

class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        {% if cookiecutter.use_cloudron_auth == "yes" %}
        # Validate tokens from Cloudron OAuth
        try:
            social_token = SocialToken.objects.get(token=token)
            if social_token.account.provider == 'openid_connect':
                return social_token.account.user
        except SocialToken.DoesNotExist:
            pass
        {% endif %}

        # Add additional token validation logic here if needed
        return None

api = NinjaAPI(
    title="{{ cookiecutter.project_name }} API",
    version="{{ cookiecutter.version }}",
    description="""
    {{ cookiecutter.description }}
    
    Authentication:
    - Bearer token authentication {% if cookiecutter.use_cloudron_auth == "yes" %}(via Cloudron OAuth){% endif %}
    - API key authentication for service accounts
    """,
    auth=[ApiKey(), BearerAuth()],
    csrf=True,  # Enable CSRF protection
    docs=Redoc(),  # Use Redoc for API documentation
    docs_url="/docs/",  # Access API docs at /api/docs
    # OpenAPI docs customization
    openapi_extra={
        "info": {
            "contact": {
                "name": "{{ cookiecutter.author_name }}",
                "email": "{{ cookiecutter.author_email }}"
            },
            "x-logo": {
                "url": "/static/img/logo.png"
            }
        }
    }
)
