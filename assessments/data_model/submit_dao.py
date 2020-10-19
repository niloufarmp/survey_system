__author__ = "Niloufar MP"

import logging
from typing import List

from django.db import DatabaseError

from assessments.exceptions.internal_exception import InternalException
from assessments.objectmodel.submit import Submit


class SubmitDao:
    logger = logging.getLogger(__name__)

    def save(self, submit: Submit) -> None:
        try:
            submit.save()
        except DatabaseError as e:
            self.logger.fatal(f'Failed to save assessment with id {submit.assessment_id}, cause {e}', exc_info=True)
            raise InternalException

    def load(self, assessment_id: str) -> List[Submit]:
        try:
            submit_list: List[Submit] = Submit.objects.filter(survey_id=assessment_id)
            return submit_list
        except Submit.DoesNotExist:
            self.logger.info(f'No submit for assessment with id {assessment_id}')
            return []
