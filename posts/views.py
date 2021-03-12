from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from posts import filters
from posts.models import Post, Favourite, User, Hashtags
from posts.permissions import IsOwner
from posts.serializers import (
    PostSerializer,
    LikePostSerializer,
    UnlikePostSerializer,
    UnfavourPostSerializer,
    FavouriteSerializer,
    UserSerializer,
    UserSerializerWithToken,
    FavourPostSerializer,
)


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_class = filters.PostFilter
    filter_fields = ('likes',)

    def get_permissions(self):
        if self.request.method == 'PATCH':
            self.permission_classes = (IsOwner)
        if self.request.method == 'DELETE':
            self.permission_classes = (IsOwner)
        return super(NetworkViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = self.queryset
        hashtags = self.request.query_params.get('hashtags', [])
        if isinstance(hashtags, str):
            hashtags = hashtags.split(',')
            queryset = queryset.filter(
                id__in=Hashtags.objects.filter(hashtag__in=hashtags).distinct().values('posts')
            )
            return queryset
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # pass current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def like(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = LikePostSerializer(
            instance,
            context={
                'request': request
            },
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def unlike(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = UnlikePostSerializer(
            instance,
            context={
                'request': request
            },

            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def favor(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = FavourPostSerializer(
            instance,
            context={
                'request': request
            },
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def unfavour(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = UnfavourPostSerializer(
            instance,
            context={
                'request': request
            },
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def favourites(self, request, *args, **kwargs):
        current_user = request.user
        queryset = Favourite.objects.filter(author=current_user)
        serializer = FavouriteSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class UserViewSet(
    viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserSerializerWithToken(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=["GET"])
    def current_user(self, request):
        """
        Determine the current user by their token, and return their data
        """
        serializer = self.get_serializer(request.user)

        return Response(serializer.data)
