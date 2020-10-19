__author__ = "Niloufar MP"

from django import forms

from assessments.objectmodel.assessment import Assessment


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name']
