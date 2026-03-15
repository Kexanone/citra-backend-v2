from time import time

from rest_framework import serializers

from .models import Player, Room


def get_client_ip(request):
    """
    Return IP of the client
    """
    if 'HTTP_X_REAL_IP' in request.META:
        return request.META['HTTP_X_REAL_IP']
    elif 'REMOTE_ADDR' in request.META:
        return request.META['REMOTE_ADDR']

    return ''


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for Room model
    """

    address = serializers.IPAddressField(read_only=True)
    owner = serializers.CharField(read_only=True)
    timestamp = serializers.IntegerField(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        """
        Postprocessing response data:
        - Replace internal id with externalGuid
        - Remove all fields with null
        """
        data = super().to_representation(instance)
        data['id'] = data['externalGuid']
        return {key: value for key, value in data.items() if value is not None}

    def create(self, validated_data):
        """
        Add metadata on creation:
        - "address": From sender IP
        - "owner": From auth user
        - "timestamp": Current time
        """
        request = self.context.get('request')
        validated_data['address'] = get_client_ip(request)
        validated_data['owner'] = request.user.username
        validated_data['timestamp'] = int(time())
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update metadata on update:
        - "address": From sender IP
        - "timestamp": Current time
        """
        instance = super().update(instance, validated_data)
        request = self.context.get('request')
        instance.address = get_client_ip(request)
        instance.timestamp = int(time())
        instance.save()
        return instance

    def validate_players(self, value):
        """
        Validate players with the PlayerSerializer
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("'players' field must be a list.")

        players_serializer = PlayerSerializer(data=value, many=True)

        if not players_serializer.is_valid():
            raise serializers.ValidationError(players_serializer.errors)

        return players_serializer.validated_data


class PlayerSerializer(serializers.ModelSerializer):
    """
    Helper serializer for validating entries in "players" field
    """

    # Enforce that even PATCH has to provide these fields
    nickname = serializers.CharField(required=True)
    gameName = serializers.CharField(required=True, allow_blank=True)
    gameId = serializers.IntegerField(required=True)

    class Meta:
        model = Player
        fields = '__all__'
