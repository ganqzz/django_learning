from django.contrib.auth.models import User
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter
from django_filters import rest_framework as filters  # 3.7~
# from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle

from .models import Game
from .models import GameCategory
from .models import Player
from .models import PlayerScore
from .permissions import IsOwnerOrReadOnly
from .serializers import GameCategorySerializer
from .serializers import GameSerializer
from .serializers import PlayerScoreSerializer
from .serializers import PlayerSerializer
from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)
    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    filter_fields = (
        'name',
        'game_category',
        'release_date',
        'played',
        'owner',
    )
    search_fields = ('^name',)
    ordering_fields = ('name', 'release_date',)

    def perform_create(self, serializer):
        # Pass an additional owner field to the create method
        # To Set the owner to the user received in the request
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly)


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'
    filter_fields = ('name', 'gender',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreFilter(filters.FilterSet):
    min_score = NumberFilter(
        name='score', lookup_expr='gte')
    max_score = NumberFilter(
        name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(
        name='score_date', lookup_expr='gte')
    to_score_date = DateTimeFilter(
        name='score_date', lookup_expr='lte')
    player_name = AllValuesFilter(
        name='player__name')
    game_name = AllValuesFilter(
        name='game__name')

    class Meta:
        model = PlayerScore
        fields = (
            'score',
            'from_score_date',
            'to_score_date',
            'min_score',
            'max_score',
            # player__name will be accessed as player_name
            'player_name',
            # game__name will be accessed as game_name
            'game_name',
        )


class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'
    filter_class = PlayerScoreFilter
    ordering_fields = ('score', 'score_date',)


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request),
            'users': reverse(UserList.name, request=request),
        })
