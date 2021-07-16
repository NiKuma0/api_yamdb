from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(http_method_names=('GET',))
def some_view(request):
    return Response(data={'detail': 'hello world'})
