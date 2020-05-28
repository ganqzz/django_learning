from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes([AllowAny])
def top(request):
    return Response({
        'admin': reverse('admin:index', request=request),
        'locations': reverse('api-root', request=request),
    })
