from django.db import transaction
from django.utils import timezone
from rest_framework.serializers import (
    IntegerField, ModelSerializer, Serializer, ValidationError,
)

from polls.models import Choice, Question


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text']


class ChoiceAdminSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']
        read_only_fields = ['votes']


class QuestionSerializer(ModelSerializer):

    choices = ChoiceSerializer(source='choice_set', many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'choices']


class QuestionAdminSerializer(ModelSerializer):

    choices = ChoiceAdminSerializer(source='choice_set', many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'choices']
        read_only_fields = ['pub_date']

    def validate_choices(self, value):
        if len(value) < 2:
            raise ValidationError('Au moins 2 choix sont requis.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        choices = validated_data.pop('choice_set')
        question = Question.objects.create(pub_date=timezone.now(), **validated_data)
        Choice.objects.bulk_create(Choice(question=question, **c) for c in choices)
        return question


class VoteSerializer(Serializer):

    choice = IntegerField()
