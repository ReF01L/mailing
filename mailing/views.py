from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Client, Mailing
from .serializers import ClientSerializer, MailingSerializer


class ClientAPIView(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingAPIView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def update_query_set(self, pk: int = None) -> filter:
        result = self.queryset.values()
        for idx in range(len(result)):
            elem = result[idx]['dispatch'] = {}
            elem['Complete'] = self.queryset[idx].dispatch.filter(status='Complete').values()
            elem['InProcess'] = self.queryset[idx].dispatch.filter(status='InProcess').values()
            elem['Error'] = self.queryset[idx].dispatch.filter(status='Error').values()
        return filter(lambda x: x['id'] == pk, result) if pk else result

    def list(self, request, *args, **kwargs):
        return Response({'data': self.update_query_set()}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response({'data': self.update_query_set(int(kwargs['pk']))}, status=status.HTTP_200_OK)
