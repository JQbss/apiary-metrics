from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from yaml import serialize

from apps.queen_notes.serializers import QueenNoteSerializer
from apps.queens.models import Queen


class QueenNotesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QueenNoteSerializer

    def get_queryset(self):
        user = self.request.user
        return self.serializer_class.Meta.model.objects.filter(queen__hive__apiary__user=user).select_related(
            'queen__hive__apiary')

    @extend_schema(
        summary='Create a new queen note',
        description='Create a new queen note for existing queen',
        responses={
            201: QueenNoteSerializer,
            400: 'Bad Request',
        },
    )
    def create(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='queen_id',
                type=int,
                description='Filter by queen ID',
                required=False,
            )
        ],
        summary='List all queen notes',
        description='Retrieve a list of all queen notes for the authenticated user',
        responses={
            200: QueenNoteSerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        queen_id = request.query_params.get('queen_id')
        if queen_id:
            try:
                queen = Queen.objects.get(
                    id=queen_id,
                    hive__apiary__users=request.user
                )
                queen_notes = self.serializer_class.Meta.model.objects.filter(queen=queen)
            except Queen.DoesNotExist:
                return Response({'detail': 'Queen not found'}, status=404)
        else:
            queen_notes = self.serializer_class.Meta.model.objects.filter(
                queen__hive__apiary__users=request.user
            )

        queen_notes = queen_notes.select_related('queen__hive__apiary')
        serializer = self.serializer_class(
            queen_notes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @extend_schema(
        summary='Retrieve a specific queen note',
        description='Retrieve a specific queen note by ID',
        responses={
            200: QueenNoteSerializer,
            401: 'Unauthorized',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            queen_note = self.serializer_class.Meta.model.objects.get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary_id=queen_note.queen.hive.apiary.id,
                    role__in=['ADMIN', 'OWNER', 'EDITOR', 'VIEWER']
            ).exists():
                return Response({'detail': 'Not authorized to access this queen note'}, status=403)
            serializer = self.serializer_class(
                queen_note,
                context={'request': request}
            )
            return Response(serializer.data)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Queen note not found'}, status=404)

    @extend_schema(
        summary='Update a queen note',
        description='Update an existing queen note',
        responses={
            200: QueenNoteSerializer,
            400: 'Bad Request',
            404: 'Not Found',
        },
    )
    def update(self, request, pk=None):
        try:
            queen_note = self.serializer_class.Meta.model.objects.get(pk=pk)
            serializer = self.serializer_class(
                queen_note,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Queen note not found'}, status=404)
