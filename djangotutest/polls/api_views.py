from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from polls.models import Question
from polls.serializers import QuestionSerializer, QuestionAdminSerializer, VoteSerializer


class QuestionViewSet(ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return (
            Question.objects.filter(pub_date__lte=timezone.now())
            .prefetch_related('choice_set')
            .order_by('-pub_date')
        )

    @action(detail=True, methods=['post'])
    def vote(self, request, pk):
        question = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = question.choice_set.filter(
            pk=serializer.validated_data['choice']
        ).update(votes=F('votes') + 1)
        if not updated:
            return Response(
                {'choice': 'Choix invalide pour ce sondage.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'detail': 'Vote enregistré.'})


class AdminQuestionViewSet(ModelViewSet):
    serializer_class = QuestionAdminSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Question.objects.prefetch_related('choice_set').order_by('-pub_date')
