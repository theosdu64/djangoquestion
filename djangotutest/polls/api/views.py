from django.db.models import F
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from polls.models import Question

from .serializers import QuestionSerializer, VoteSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Public : list, retrieve, vote.
    Authentifié : create (liste/détail avec le nombre de votes).
    """

    serializer_class = QuestionSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return (
            Question.objects.filter(pub_date__lte=timezone.now())
            .prefetch_related("choice_set")
            .order_by("-pub_date")
        )

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        question = self.get_object()
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = question.choice_set.filter(pk=serializer.validated_data["choice"]).update(
            votes=F("votes") + 1
        )
        if not updated:
            return Response(
                {"choice": "Choix invalide pour ce sondage."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"detail": "Vote enregistré."})
