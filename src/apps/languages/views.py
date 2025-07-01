from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.languages.models import Language
from apps.languages.serializers import LanguageSerializer


class LanguageViewSet(ViewSet):
    serializer_class = LanguageSerializer

    @extend_schema(
        summary='List all languages',
        description='Retrieve a list of all available languages',
        responses={
            200: LanguageSerializer(many=True),
        },
    )
    def list(self, request):
        languages = Language.objects.all()
        serializer = self.serializer_class(languages, many=True)
        return Response(serializer.data)
