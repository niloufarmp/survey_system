__author__ = "Niloufar MP"

from django import forms

from assessments.objectmodel.question import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['description']
