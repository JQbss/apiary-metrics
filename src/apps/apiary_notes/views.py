from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.apiary_notes.serializers import ApiaryNoteSerializers


class ApiaryNotesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ApiaryNoteSerializers

    def get_queryset(self):
        user = self.request.user
        return self.serializer_class.Meta.model.objects.filter(apiary__users=user).select_related('apiary')

    @extend_schema(
        summary='Create a new apiary note',
        description='Create a new apiary note for existing apiary',
        responses={
            201: ApiaryNoteSerializers,
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
                name='apiary_id',
                type=int,
                description='Filter by apiary ID',
                required=False,
            )
        ],
        summary='List all apiary notes',
        description='Retrieve a list of all apiary notes for the authenticated user',
        responses={
            200: ApiaryNoteSerializers(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        apiary_id = request.query_params.get('apiary_id')
        if apiary_id:
            queryset = self.get_queryset().filter(apiary__id=apiary_id)
        else:
            queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Retrieve a specific apiary note',
        description='Retrieve a specific apiary note by ID',
        responses={
            200: ApiaryNoteSerializers,
            404: 'Not Found',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            apiary_note = self.get_queryset().get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary=apiary_note.apiary,
                    role__in=['ADMIN', 'OWNER', 'EDITOR', 'VIEWER']
            ).exists():
                return Response({'detail': 'You do not have permission to view this apiary note.'}, status=403)
            serializer = self.serializer_class(
                apiary_note,
                context={'request': request}
            )
            return Response(serializer.data)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Apiary note not found'}, status=404)


    @extend_schema(
        summary='Update an apiary note',
        description='Update an existing apiary note by ID',
        responses={
            200: ApiaryNoteSerializers,
            400: 'Bad Request',
            404: 'Not Found',
        },
    )
    def update(self, request, pk=None):
        try:
            apiary_note = self.serializer_class.Meta.model.objects.get(pk=pk)
            serializer = self.serializer_class(
                apiary_note,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Apiary note not found'}, status=404)