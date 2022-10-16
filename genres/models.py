from django.db import models
from django.forms import CharField


class Genre(models.Model):
    name = CharField(max_length=127)
