from django.db import models

class UserLog(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    search_term = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.search_term} at {self.timestamp}"

