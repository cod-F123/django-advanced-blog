from django.db import models
from django.utils.translation import gettext_lazy as _
from .users import User


class Profile(models.Model):
    """
    This class defines the profile model for users
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(
        verbose_name=_("First Name"), max_length=255, blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"), max_length=255, blank=True, null=True
    )

    bio = models.TextField(verbose_name=_("Bio"), blank=True, null=True)

    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="user/profile/images",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.email
