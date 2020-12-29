from django.db import models
from django.contrib.auth.models import User

class Mood(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    score = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__gte=1) & models.Q(score__lte=5),
                name="score constraint",
            )
        ]
