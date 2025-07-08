from rest_framework import viewsets

from .serializers import ComponentSerializer
from .models import Component


class ComponentViewSet(viewsets.ModelViewSet):

    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


        

