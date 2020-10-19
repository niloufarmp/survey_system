from django.urls import path

from assessments.views import report_view, submission_view, management_view, main_view

urlpatterns = [
    path('', main_view.main, name='main'),
    path('assessments/', management_view.new_assessment, name='new_assessment'),
    path('assessments/<str:assessment_id>/questions/', management_view.questions_management,
         name='questions_management'),
    path('assessments/<str:assessment_id>/formula/', management_view.assessment_formula, name='assessment_formula'),
    path('assessments/<str:assessment_id>/', submission_view.complete_assessment, name='complete_assessment'),
    path('assessments/<str:assessment_id>/report/', report_view.submission_summary, name='report'),
]
