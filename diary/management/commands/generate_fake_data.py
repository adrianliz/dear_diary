import random

from django.db import transaction
from django.core.management.base import BaseCommand

from .factories import UserFactory, MoodFactory, ProfileFactory, AdviceFactory

NUM_USERS = 10
NUM_MOODS = 400
NUM_ADVICES = 8

class Command(BaseCommand):
    help = "Generates fake data for Dear Diary"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Generating fake data...")

        users = []
        for _ in range(NUM_USERS):
            user = UserFactory()
            ProfileFactory(user=user)
            users.append(user)

        for _ in range(NUM_MOODS):
            user = random.choice(users)
            MoodFactory(user=user)

        for _ in range(NUM_ADVICES):
            AdviceFactory()

        self.stdout.write("Fake data generated")