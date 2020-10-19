__author__ = "Niloufar MP"

from django import forms


class AnswerForm(forms.Form):
    answer = forms.IntegerField(required=True, min_value=1, max_value=5)

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].label = self.initial['description'] if 'description' in self.initial.keys() else ''
