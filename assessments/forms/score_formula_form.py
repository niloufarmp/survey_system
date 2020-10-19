__author__ = "Niloufar MP"

from django import forms


class ScoreFormulaForm(forms.Form):
    score_formula = forms.CharField(required=False, empty_value=None)
