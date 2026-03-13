from django.urls import path
from .views import get_public_key, ExternalTokenObtainView, InternalTokenObtainView

urlpatterns = [
    path('external/key.pem', get_public_key),
    path("external/<uuid:externalGuid>", ExternalTokenObtainView.as_view(), name="external_token_obtain"),
    path('internal', InternalTokenObtainView.as_view(), name='internal_token_obtain'),
]
