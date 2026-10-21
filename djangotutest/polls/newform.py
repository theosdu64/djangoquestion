from django import forms
from .models import Choice, Question

class QuestionFormModel(forms.ModelForm):

    class Meta:
        model = Question
        fields = ["question_text", "pub_date"]

class ChoiceForm(forms.Form):
    choice1 = forms.CharField(label="Choix 1")
    choice2 = forms.CharField(label="Choix 2")
    choice3 = forms.CharField(label="Choix 3", required=False)
    choice4 = forms.CharField(label="Choix 4", required=False)
    choice5 = forms.CharField(label="Choix 5", required=False)