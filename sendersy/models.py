from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    content = models.TextField(max_length=120)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    by = models.CharField(max_length=25, default='Anonymous')
    
    def __str__(self):
        return str(self.to).capitalize() + ' -' + str(self.by)