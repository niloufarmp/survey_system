__author__ = "Niloufar MP"

from django.db import models

from assessments.objectmodel.assessment import Assessment


class Question(models.Model):
    description = models.CharField(max_length=255)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, to_field='UUID')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
