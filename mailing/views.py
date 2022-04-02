from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Client
from .serializers import ClientSerializer


class ClientAPIView(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
