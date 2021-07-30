from django.db import models

class SiteWide(models.Model):
    sitename = models.CharField(max_length=255, default='ChangeMe')
    
    def __str__(self):
        return self.sitename


