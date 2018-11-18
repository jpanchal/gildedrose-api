from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class Itemlist(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.CharField(max_length=255, null=True, unique=False)
    price = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField(null=True)
    owner = models.ForeignKey(
        'auth.User',
        related_name='itemlists',
        on_delete=models.CASCADE)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


class Cart(models.Model):
    item = models.ForeignKey('Itemlist', related_name='cart', on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=False, default=0)
    owner = models.ForeignKey(
        'auth.User',
        related_name='cart',
        on_delete=models.CASCADE)


# This receiver handles token creation when a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
