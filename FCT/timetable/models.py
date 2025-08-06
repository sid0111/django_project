from django.db import models
import uuid
from django.contrib.auth.models import User

class Topic(models.Model):
    """
    A model to represent a topic learned by the user.
    Each topic is now associated with a specific user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    learned_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name