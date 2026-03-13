from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid import uuid4

PORT_VALIDATORS = [MinValueValidator(1), MaxValueValidator(65535)]

class Room(models.Model):
    '''
    Model for a room in the DB
    '''
    externalGuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    address = models.GenericIPAddressField()
    port = models.IntegerField(validators=PORT_VALIDATORS)
    owner = models.TextField()
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    preferredGameName = models.TextField(blank=True)
    preferredGameId = models.BigIntegerField()
    maxPlayers = models.IntegerField()
    netVersion = models.IntegerField()
    hasPassword = models.BooleanField()
    players = models.JSONField(blank=True, null=True)
    timestamp = models.BigIntegerField()

class Player(models.Model):
    '''
    Helper model for validating entries in "players" field
    '''
    username = models.TextField(blank=True, null=True)
    avatarUrl = models.URLField(blank=True, null=True)
    nickname = models.TextField()
    gameName = models.TextField(blank=True)
    gameId = models.BigIntegerField()

    class Meta:
        # This model is for validation only
        managed = False
