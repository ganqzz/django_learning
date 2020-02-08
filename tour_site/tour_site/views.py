from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def top(request):
    return Response({
        'admin': reverse('admin:index', request=request),
        'api_v1': reverse('apiv1:api-root', request=request),
    })
