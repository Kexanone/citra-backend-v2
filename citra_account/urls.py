from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import ChangeAvatarView, GenerateTokenView, DeleteUserView, get_avatar

urlpatterns = [
    path('', RedirectView.as_view(url='avatar/change/', permanent=False)),
    path('', include('allauth.urls')),
    path('avatar/change/', ChangeAvatarView.as_view(), name="account_change_avatar"),
    path('avatars/<str:username>.png', get_avatar),
     path('token/', GenerateTokenView.as_view(), name="generate_token"),
    path('delete/', DeleteUserView.as_view(), name='delete_account'),
]
