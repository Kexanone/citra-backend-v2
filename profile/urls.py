from django.urls import include, path

from .views import ChangeAvatarView, get_avatar

urlpatterns = [
    path('', include('allauth.urls')),
    path(
        'avatar/change/',
        ChangeAvatarView.as_view(),
        name='account_change_avatar',
    ),
    path('avatars/<int:user_id>.png', get_avatar),
]
