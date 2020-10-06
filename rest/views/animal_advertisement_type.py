from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from listanimal.models import AnimalType
from rest.serializer import AnimalTypeSerializer


class AnimalAdvertisementTypeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self):

        type = AnimalType.objects.all()
        serializer = AnimalTypeSerializer(type,many=True)
        return Response(serializer.data)