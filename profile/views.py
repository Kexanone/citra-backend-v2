from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView

from .forms import ChangeAvatarForm
from .models import Profile


class ChangeAvatarView(LoginRequiredMixin, UpdateView):
    """
    View for logged in users to change their avatar
    """

    model = Profile
    template_name = 'account/avatar_change.html'
    form_class = ChangeAvatarForm
    success_url = '/profile/avatar/change/'

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        return super().form_valid(form)


def get_avatar(request, user_id):
    """
    Returns the avatar for the given user
    """
    profile = get_object_or_404(Profile, user__id=user_id)

    if not profile.avatar:
        raise Http404('Avatar not found')

    with profile.avatar.open('rb') as stream:
        content = stream.read()

    return HttpResponse(content, content_type='image/png')
