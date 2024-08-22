from django.db import models

class Log(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    ip_address = models.GenericIPAddressField()
    wallet_address = models.CharField(max_length=50)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address}:{self.wallet_address}:{self.status}:{self.transaction_id}:{self.created_at}"
