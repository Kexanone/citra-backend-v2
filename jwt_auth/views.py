from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from citra_account.models import Account, get_user_from_token
from pathlib import Path

def get_public_key(request):
    '''
    Returns public key that is used for signing JWT
    '''
    key_path = Path(__file__).parent / 'keys/jwt_public.pem'

    with key_path.open('rb') as stream:
        public_key = stream.read()

    return HttpResponse(public_key, content_type='text/plain')

def get_user_from_header(request):
    '''
    Returns user from 'X-Token' header
    '''
    token = request.META.get('HTTP_X_TOKEN')

    if not token:
        raise AuthenticationFailed('Missing "X-Token" in headers')

    user = get_user_from_token(token)

    if user is None:
        raise AuthenticationFailed('Invalid token')
    
    return user

class InternalTokenObtainView(APIView):
    '''
    Tries to get JWT for user from header
    If this fails, JWT for anonymous user is returned
    '''
    def post(self, request, *args, **kwargs):
        try:
            user = get_user_from_header(request)
        except AuthenticationFailed:
            user = User.objects.get(username='anonymous')

        refresh = RefreshToken.for_user(user)
        return HttpResponse(refresh.access_token)

class ExternalTokenObtainView(APIView):
    '''
    Tries to get JWT for user from header
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, externalGuid):
        refresh = RefreshToken.for_user(request.user)
        refresh['aud'] = f'external-{externalGuid}'
        refresh['username'] = request.user.username

        try:
            account = request.user.account
            refresh['avatarUrl'] = request.build_absolute_uri(account.avatar_url)
        except Account.DoesNotExist:
            pass

        return HttpResponse(refresh.access_token)
