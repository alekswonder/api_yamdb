from rest_framework.pagination import PageNumberPagination


class ComplexObjectPagination(PageNumberPagination):
    """Расширение для PageNumberPagination, которое будет отображать
     значительно меньше объектов на странице, хранящих в себе большое
    количество информации
    """
    page_size = 5
