__author__ = "Niloufar MP"

from uuid import uuid4

from django.db import models


class Assessment(models.Model):
    name = models.CharField(max_length=100)
    UUID = models.UUIDField(default=uuid4, unique=True)
    score_formula = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
