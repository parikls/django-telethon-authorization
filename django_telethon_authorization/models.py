from django.contrib.auth import get_user_model
from django.db import models


class TelegramAuthorization(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    phone = models.CharField(max_length=254)
    code = models.IntegerField(null=True, blank=True)
    phone_code_hash = models.CharField(max_length=254, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone