from django.db import models
from django.utils.timezone import now

class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()  # Size in bytes
    path = models.TextField()  # File path on disk
    folder = models.ForeignKey('api.Folder', on_delete=models.CASCADE, related_name='files')  # String reference
    user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='files')  # String reference
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.name