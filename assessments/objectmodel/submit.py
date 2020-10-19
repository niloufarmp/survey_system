__author__ = "Niloufar MP"

from typing import List

from django.db import models
from jsonfield import JSONField

from assessments.objectmodel.assessment import Assessment


class Submit(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, to_field='UUID')
    score = models.FloatField(blank=True)
    answers = JSONField()
    error = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def set_answers(self, answer_list: List[str]):
        self.answers = [int(answer) for answer in answer_list]
