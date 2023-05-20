from django.db import models
from profiles.models import UserProfile
from products.models import Product


class Wishlist(models.Model):
    profile = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Wishlist ({self.profile})'
