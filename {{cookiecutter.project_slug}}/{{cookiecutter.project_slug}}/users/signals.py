from allauth.account.signals import user_signed_up
{% if cookiecutter.use_cloudron_auth == "yes" %}from allauth.socialaccount.signals import social_account_added{% endif %}
from django.dispatch import receiver


@receiver(user_signed_up)
def handle_user_signed_up(sender, request, user, **kwargs):
    """Handle post-signup actions."""
    # Add any post-signup logic here
    pass

{% if cookiecutter.use_cloudron_auth == "yes" %}
@receiver(social_account_added)
def handle_social_account_added(sender, request, sociallogin, **kwargs):
    """Handle Cloudron account connection."""
    if sociallogin.account.provider == 'openid_connect':
        user = sociallogin.user
        # Store Cloudron user ID
        user.cloudron_user_id = sociallogin.account.uid
        user.save()
{% endif %}
