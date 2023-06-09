from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLine

# signals are sent after a model is saved or deleted


@receiver(post_save, sender=OrderLine)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_fintotal()


@receiver(post_delete, sender=OrderLine)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_fintotal()
