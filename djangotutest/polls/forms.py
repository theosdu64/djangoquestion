from django import forms

class QuestionForm(forms.Form):
    question_text = forms.CharField(label="Question")

    choice1 = forms.CharField(label="Choix 1", required=False)
    choice2 = forms.CharField(label="Choix 2", required=False)
    choice3 = forms.CharField(label="Choix 3", required=False)
    choice4 = forms.CharField(label="Choix 4", required=False)
    choice5 = forms.CharField(label="Choix 5", required=False)