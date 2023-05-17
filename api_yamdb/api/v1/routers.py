from rest_framework.routers import Route, SimpleRouter


class CustomRRetrieveUpdateUserRouter(SimpleRouter):
    '''Кастомный роутер для отображения retrieve объекта не по pk, а по me.'''

    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        )
    ]
