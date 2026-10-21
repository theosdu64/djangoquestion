from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from polls.models import Choice, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "choice_text", "votes"]
        read_only_fields = ["votes"]


class QuestionSerializer(serializers.ModelSerializer):
    """Les votes ne sont visibles que pour un utilisateur authentifié."""

    choices = ChoiceSerializer(source="choice_set", many=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date", "choices"]
        read_only_fields = ["pub_date"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if not (request and request.user.is_authenticated):
            for choice in data["choices"]:
                choice.pop("votes", None)
        return data

    def validate_choices(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Au moins 2 choix sont requis.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        choices = validated_data.pop("choice_set")
        question = Question.objects.create(pub_date=timezone.now(), **validated_data)
        Choice.objects.bulk_create(Choice(question=question, **c) for c in choices)
        return question


class VoteSerializer(serializers.Serializer):
    choice = serializers.IntegerField()
