from django.shortcuts import render, redirect

from assessments.data_model.assessment_dao import AssessmentDao
from assessments.data_model.submit_dao import SubmitDao

submit_dao = SubmitDao()
assessment_dao = AssessmentDao()


def main(request):
    if request.method == 'POST':
        return redirect('complete_assessment', request.POST['assessment_id'])
    return render(request, "index.html", {'title': 'Home'})
