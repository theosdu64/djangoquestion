from django import forms
from .models import Question

class QuestionForm(forms.Form):
    question_text = forms.CharField(label="Titre de la question", max_length=200)
    pub_date = forms.DateField(label="Date de la publication", widget=forms.DateInput(attrs={'type': 'date'}))
    choice1 = forms.CharField(label="Choix 1", required=False)
    choice2 = forms.CharField(label="Choix 2", required=False)
    choice3 = forms.CharField(label="Choix 3", required=False)
    choice4 = forms.CharField(label="Choix 4", required=False)
    choice5 = forms.CharField(label="Choix 5", required=False)

    # class Meta:
    #     model = Question
    #     fields = ["question_text"]
    #     labels = {
    #         "question_text": "Votre question"
    #     }
    #     widgets = {
    #         "question_text": forms.TextInput(attrs={
    #             "class": "form-control",
    #             "placeholder": "Votre question",
    #         }), 
    #     }