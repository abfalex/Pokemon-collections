from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.TextField(max_length=200)
