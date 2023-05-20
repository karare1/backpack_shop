from django.db import models
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    subject = models.CharField(max_length=255, null=False, blank=False)
    message = models.TextField(max_length=5000, null=False, blank=False)
    sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.email
