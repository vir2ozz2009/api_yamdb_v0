"""Кастомные миксины и вьюсеты."""

from rest_framework import mixins, viewsets, filters

from .permissions import OnlyAdminPermission


class DestroyCreateListMixins(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Кастомный миксин для вьюсетов моделей Category и Genre."""

    permission_classes = (OnlyAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """Кастомный родительский ViewSet для наследования."""

    def get_object(self):
        return self.request.user
