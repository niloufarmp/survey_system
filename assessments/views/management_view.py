__author__ = "Niloufar MP"

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render, redirect

from assessments.data_model.assessment_dao import AssessmentDao
from assessments.exceptions.internal_exception import InternalException
from assessments.exceptions.not_found_exception import NotFoundException
from assessments.forms.assessment_form import AssessmentForm
from assessments.forms.question_form import QuestionForm
from assessments.forms.score_formula_form import ScoreFormulaForm
from assessments.objectmodel.assessment import Assessment
from assessments.util.score import Score

assessment_dao = AssessmentDao()
TITLE = 'New Assessment'


def new_assessment(request):
    try:
        if request.method == "POST":
            form = AssessmentForm(request.POST)

            if form.is_valid():
                assessment: Assessment = form.save(commit=False)
                assessment_dao.save(assessment)
                return redirect('questions_management', assessment_id=assessment.UUID)
        else:
            form = AssessmentForm()
        context = {
            'form': form,
            'title': TITLE
        }
        return render(request, "assessments/new_assessment.html", context)
    except InternalException as e:
        return HttpResponseServerError(e)


def questions_management(request, assessment_id):
    assessment: Assessment = assessment_dao.load(assessment_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.assessment_id = assessment_id
            question.save()
    else:
        form = QuestionForm()
    context = {
        'assessment': assessment,
        'question_form': form,
        'title': TITLE
    }
    return render(request, "assessments/questions_management.html", context)


def assessment_formula(request, assessment_id):
    try:
        assessment: Assessment = assessment_dao.load(assessment_id)
        if request.method == "POST":
            form = ScoreFormulaForm(request.POST)
            if form.is_valid():
                try:
                    assessment.score_formula = form.cleaned_data['score_formula']
                    Score.validate_formula(assessment)
                    assessment.save()
                    return redirect('report', assessment_id=assessment_id)
                except ValidationError as e:
                    form.add_error("score_formula", e)
        else:
            form = ScoreFormulaForm()
        context = {'form': form, 'assessment': assessment,
                   'title': TITLE
                   }
        return render(request, 'assessments/assessment_formula.html', context)
    except NotFoundException as e:
        return HttpResponseNotFound(e)
    except InternalException as e:
        return HttpResponseServerError(e)
