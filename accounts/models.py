from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUser(AbstractUser):
    mobile = models.CharField(null=True, blank=True, max_length=16)

    def __str__(self):
        return '{} ({})'.format(self.username, self.email)
