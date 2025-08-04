from django.db import models
import uuid

class Topic(models.Model):
    """
    A model to represent a topic learned by the user.
    Each topic has a name and the date it was learned.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    learned_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
