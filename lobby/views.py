from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Room
from .serializers import RoomSerializer
from .permissions import IsObjectOwner


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'externalGuid'

    def list(self, request, *args, **kwargs):
        '''
        Wrap list of rooms in an object
        '''
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({"rooms": serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        '''
        Return empty JSON on successful DELETE
        '''
        response = super().destroy(request, *args, **kwargs)

        if response.status_code != status.HTTP_204_NO_CONTENT:
            return response

        return JsonResponse({})

    def get_permissions(self):
        '''
        No authentication for list action
        Others are limited to owner
        '''
        if self.action == 'list':
            return [AllowAny()]

        return [IsAuthenticated(), IsObjectOwner()]
