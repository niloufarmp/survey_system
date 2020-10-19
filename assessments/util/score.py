__author__ = "Niloufar MP"

import logging
import re
from typing import List

from django.core.exceptions import ValidationError

from assessments.objectmodel.assessment import Assessment
from assessments.objectmodel.submit import Submit


class Score:
    logger = logging.getLogger(__name__)

    @staticmethod
    def average(submit_list: List[Submit]):
        number_of_submits = len(submit_list)
        if number_of_submits > 0:
            all_scores = [submit.score for submit in submit_list if not submit.error]
            average_score = sum(all_scores) / number_of_submits
            return round(average_score, 2)
        else:
            return 0

    @classmethod
    def get_submits_containing_score_error(cls, submit_list: List[Submit]) -> List[Submit]:
        return [submit for submit in submit_list if submit.error]

    def calculate(self, submit: Submit) -> None:
        score = 0
        try:
            formula = submit.assessment.score_formula
            if formula:
                score = self._execute_formula(formula, submit)
            else:
                submit.error = 'Assessment does not have score.'
        except RuntimeError as e:
            self.logger.warning(e)
            submit.error = e
        except SyntaxError:
            message = 'Error in provided Formula.'
            self.logger.fatal(message, exc_info=True)
            submit.error = message
        finally:
            submit.score = score

    @classmethod
    def validate_formula(cls, assessment: Assessment):
        questions_count: int = len(assessment.question_set.all())
        formula: str = assessment.score_formula
        if formula:
            cls._validate_formula_pattern(formula)
            cls._validate_formula_against_questions(formula, questions_count)

    @classmethod
    def _validate_formula_pattern(cls, formula: str) -> None:
        regex = '^(( )*(Q|)\d+( )*(\+|-|\*|\/))*( )*(Q|)\d+( )*$'
        pattern = re.compile(regex)
        if pattern.match(formula) is None:
            cls.logger.warning(
                f"Formula pattern is invalid, formula: {formula}")
            raise ValidationError("Formula pattern is invalid. Sample valid option: Q1 + 2*Q2")

    @classmethod
    def _validate_formula_against_questions(cls, formula: str, questions_count: int) -> None:
        question_numbers = re.findall(r'Q(\d+)', formula)
        if not all(int(number) <= questions_count for number in question_numbers):
            cls.logger.warning(
                f"Formula does not match the questions, formula: {formula}, number of questions: {questions_count}")
            raise ValidationError("Formula doesn't match the questions!")

    @staticmethod
    def _compare_formula_with_answers_index(question_number: int,
                                            answers: List[int]):
        if question_number > len(answers):
            raise RuntimeError("Formula doesn't match the questions!")

    def _generate_variables(self, question_number: int, answers: List[int], variable_names: List[str],
                            variable_values: List[str]) -> None:
        self._compare_formula_with_answers_index(question_number, answers)
        variable_names.append(f"Q{question_number}")
        variable_values.append(f"answers[{question_number}-1]")

    def _execute_formula(self, formula, submit) -> float:
        answers = submit.answers
        question_numbers = re.findall(r'Q(\d+)', formula)
        variable_names = []
        variable_values = []
        [self._generate_variables(int(number), answers, variable_names, variable_values) for number in
         question_numbers]
        exec(', '.join(variable_names) + '=' + ', '.join(variable_values))
        return eval(formula) if len(formula) > 0 else 0
