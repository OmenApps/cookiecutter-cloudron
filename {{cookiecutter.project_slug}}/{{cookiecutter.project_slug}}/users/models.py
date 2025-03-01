from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from {{ cookiecutter.project_slug }}.common.models import TimeStampedModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom User Model that uses email as the username field.
    """
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    name = models.CharField(_("full name"), max_length=255)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # MFA fields
    mfa_enabled = models.BooleanField(
        _("MFA enabled"),
        default=False,
        help_text=_("Designates whether this user has enabled multi-factor authentication."),
    )
    mfa_secret = models.CharField(
        _("MFA secret"),
        max_length=32,
        blank=True,
        help_text=_("Secret key for TOTP-based multi-factor authentication."),
    )

    # Cloudron specific fields
    {% if cookiecutter.use_cloudron_auth == "yes" %}
    cloudron_user_id = models.CharField(
        _("Cloudron user ID"),
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text=_("The user's Cloudron ID when using Cloudron authentication."),
    )
    {% endif %}
    
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        """Return the full name for the user."""
        return self.name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name.split()[0] if self.name else self.email

