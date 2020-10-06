from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from rest.serializer import AnimalInfoSerializer


class FavoritAnimal(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        queriset = request.user.favorit_animal.all()
        private_data = AnimalInfoSerializer(queriset, many=True).data
        return Response(private_data)