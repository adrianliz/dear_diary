from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Mood(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    score = models.IntegerField()
    # Necesario para que se pueda editar vía admin ya que con auto_now no se permite
    updated_on = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__gte=1) & models.Q(score__lte=5),
                name="score constraint",
            )
        ]


class Profile(models.Model):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    avatar = models.ImageField(
        upload_to='avatars/', default="avatars/noimage.png")
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, blank=True, null=True)
    public = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ContactMessage(models.Model):
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=300)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
