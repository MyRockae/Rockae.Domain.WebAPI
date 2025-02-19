from django.http import HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def debug_credentials(request):
    output = f"""
    SECRET_KEY: {settings.SECRET_KEY}<br>
    DEBUG: {settings.DEBUG}<br>
    DB_NAME: {settings.DATABASES['default']['NAME']}<br>
    DB_USER: {settings.DATABASES['default']['USER']}<br>
    DB_PASSWORD: {settings.DATABASES['default']['PASSWORD']}<br>
    DB_HOST: {settings.DATABASES['default']['HOST']}<br>
    DB_PORT: {settings.DATABASES['default']['PORT']}<br>
    """
    return HttpResponse(output)