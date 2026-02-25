from django.db import models
import datetime
from datetime import date
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return f"{self.question_text} ({self.pub_date})"

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def calcule_age(self):
        now = timezone.now()
        difference = self.pub_date - now
        return difference.days 
    
    def get_choices(self):
        choices = self.choice_set.all()
        result = []
        count = 0

        for choice in choices:
            count += choice.votes  
        for choice in choices:
            if count > 0:
                choiceproperty = choice.votes / count
            else:
                choiceproperty = 0
            result.append((choice.choice_text, int(round((choiceproperty) * 100)))) 
        return result
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text[slice(20)]