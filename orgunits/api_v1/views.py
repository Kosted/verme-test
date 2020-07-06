"""
Copyright 2020 ООО «Верме»
"""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orgunits.api_v1.serializers import OrganizationSerializer
from orgunits.models import Organization
from wfm.views import TokenAuthMixin


class OrganizationViewSet(TokenAuthMixin, ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    @action(methods=["GET"], detail=True)
    def parents(self, request, *args, **kwargs):
        """
        Возвращает родителей запрашиваемой организации
        TODO: Написать два действия для ViewSet (parents и children), используя методы модели
        """
        parents = self.get_queryset().get(id=kwargs['pk']).parents()
        res =[]
        for parent in parents:
            res.append(self.get_serializer(parent).data)

        return Response(res)

    @action(methods=["GET"], detail=True)
    def children(self, request, *args, **kwargs):
        """
        Возвращает ДЕТЕЙ запрашиваемой организации
        TODO: Написать два действия для ViewSet (parents и children), используя методы модели
        """
        children = self.get_queryset().get(id=kwargs['pk']).children()
        res =[]
        for child in children:
            res.append(self.get_serializer(child).data)

        return Response(res)
