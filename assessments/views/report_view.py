__author__ = "Niloufar MP"

from typing import List

from django.shortcuts import render

from assessments.data_model.assessment_dao import AssessmentDao
from assessments.objectmodel.assessment import Assessment
from assessments.objectmodel.statistics import Statistics
from assessments.objectmodel.submit import Submit

assessment_dao = AssessmentDao()


def submission_summary(request, assessment_id):
    assessment: Assessment = assessment_dao.load(assessment_id)
    submit_list: List[Submit] = assessment.submit_set.all()
    statistics = Statistics(assessment, submit_list)

    context = {'assessment': assessment,
               'request': request,
               'statistics': statistics,
               'title': 'Submission Summary'}
    return render(request, 'assessments/submission_summary.html', context)
