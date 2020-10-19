__author__ = "Niloufar MP"

from typing import List

from assessments.objectmodel.assessment import Assessment
from assessments.objectmodel.submit import Submit
from assessments.util.score import Score


class Statistics:
    number_of_questions: int
    average_score: float
    number_of_submits: int
    number_of_submits_containing_error: int

    def __init__(self, assessment: Assessment, submit_list: List[Submit]):
        self.number_of_questions = len(assessment.question_set.all())
        self.number_of_submits = len(submit_list)
        self.average_score = Score.average(submit_list)
        submits_containing_error: List[Submit] = Score.get_submits_containing_score_error(submit_list)
        self.number_of_submits_containing_error = len(submits_containing_error)
