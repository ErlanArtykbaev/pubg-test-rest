from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ListSerializer, HyperlinkedModelSerializer
from .models import Tournament, Rates, GameMode


class RatesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rates
        fields = ('name', 'price', 'percentage', 'kill_award', 'data', 'people_count')


class GameModeCreateSerializer(ModelSerializer):
    def create(self, validated_data):
        return GameMode.objects.create(**validated_data)

    class Meta:
        model = GameMode
        fields = '__all__'


class TournamentCreateSerializer(ModelSerializer):
    def create(self, validated_data):
        return Tournament.objects.create(**validated_data)

    class Meta:
        model = Tournament
        fields = '__all__'
