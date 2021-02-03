import factory
import random

from factory.django import DjangoModelFactory
from django.utils import timezone
from django.contrib.auth.models import User

from diary.models import Mood, Profile, Advice


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'password')
    last_login = factory.Faker(
        "date_time", tzinfo=timezone.get_current_timezone())


class MoodFactory(DjangoModelFactory):
    class Meta:
        model = Mood

    name = factory.Faker("sentence",
                         nb_words=10,
                         variable_nb_words=True)
    description = factory.Faker("sentence",
                                nb_words=100,
                                variable_nb_words=True)
    score = factory.LazyAttribute(lambda x: random.randint(1, 5))
    updated_on = factory.Faker(
        "date_time", tzinfo=timezone.get_current_timezone())
    user = factory.SubFactory(UserFactory)


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    birth_date = factory.Faker(
        "date_time", tzinfo=timezone.get_current_timezone())
    address = factory.Faker("address")
    gender = factory.LazyAttribute(lambda x: random.randint(1, 2))
    public = True
    user = factory.SubFactory(UserFactory)


class AdviceFactory(DjangoModelFactory):
    class Meta:
        model = Advice

    description = factory.Faker('sentence', nb_words=2)
    likes = factory.LazyAttribute(lambda x: random.randint(1, 20))
    user = factory.SubFactory(UserFactory)
