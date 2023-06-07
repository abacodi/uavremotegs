from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Themes
class GeneralSettings(models.Model):
    parameter = models.CharField(verbose_name="parameter", max_length=20)
    value = models.IntegerField(verbose_name="value")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    # Meta information
    class Meta:
        verbose_name = "General settings"
        unique_together = ('parameter', 'user')
    
    # Readable data
    def __str__(self):
        return self.user.first_name + ": " + self.parameter