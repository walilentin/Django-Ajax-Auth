from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
username_validator = UnicodeUsernameValidator()

class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email_verify = models.BooleanField(default=False)
    email = models.EmailField('email addres', blank=True, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
