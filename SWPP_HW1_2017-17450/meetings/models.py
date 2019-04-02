from django.db import models

class Meeting(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sinceWhen = models.DateTimeField(null=True, blank=True)
    tilWhen = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey('auth.User', related_name='meetings', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)