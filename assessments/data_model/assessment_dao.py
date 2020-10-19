__author__ = "Niloufar MP"

import logging

from django.core.exceptions import ValidationError
from django.db import DatabaseError

from assessments.exceptions.internal_exception import InternalException
from assessments.exceptions.not_found_exception import NotFoundException
from assessments.objectmodel.assessment import Assessment


class AssessmentDao:
    logger = logging.getLogger(__name__)

    def load(self, assessment_id: str) -> Assessment:
        try:
            assessment: Assessment = Assessment.objects.get(UUID=assessment_id)
            return assessment
        except ValidationError:
            raise NotFoundException(f'UUID {assessment_id} is not valid.')
        except Assessment.MultipleObjectsReturned:
            message = f'Multiple assessment objects found for id {assessment_id}'
            self.logger.fatal(message)
            raise InternalException
        except Assessment.DoesNotExist:
            self.logger.info(f'No submit for assessment with id {assessment_id}')
            raise NotFoundException(f'No assessment matches UUID {assessment_id}.')

    def save(self, assessment: Assessment):
        try:
            assessment.save()
        except DatabaseError as e:
            self.logger.fatal(f'Failed to save assessment with id {assessment.UUID}, cause {e}', exc_info=True)
            raise InternalException
