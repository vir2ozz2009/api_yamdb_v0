from rest_framework.pagination import LimitOffsetPagination


class GenresAndCategoriesPagination(LimitOffsetPagination):
    """Кастомный класс пагинации для жанров и категорий."""

    default_limit = 2
