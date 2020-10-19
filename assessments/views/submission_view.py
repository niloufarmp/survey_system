__author__ = "Niloufar MP"

from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render

from assessments.data_model.assessment_dao import AssessmentDao
from assessments.data_model.submit_dao import SubmitDao
from assessments.exceptions.internal_exception import InternalException
from assessments.exceptions.not_found_exception import NotFoundException
from assessments.objectmodel.assessment import Assessment
from assessments.objectmodel.submit import Submit
from assessments.util.score import Score

submit_dao = SubmitDao()
assessment_dao = AssessmentDao()


def complete_assessment(request, assessment_id):
    try:
        assessment: Assessment = assessment_dao.load(assessment_id)
        if request.method == 'POST':
            answer_list = request.POST.getlist('answer_list')
            submit: Submit = Submit(assessment=assessment)
            submit.set_answers(answer_list)
            Score().calculate(submit)
            submit_dao.save(submit)
            return render(request, "assessments/result.html", {'submit': submit})
        context = {
            'assessment': assessment,
            'title': 'Complete Assessment'
        }
        return render(request, "assessments/complete_assessment.html", context)
    except NotFoundException as e:
        return HttpResponseNotFound(e)
    except InternalException as e:
        return HttpResponseServerError(e)
