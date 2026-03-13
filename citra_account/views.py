from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView, DeleteView
from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from .models import Account, generate_token
from .forms import ChangeAvatarForm

username_validator = UnicodeUsernameValidator()

class ChangeAvatarView(LoginRequiredMixin, UpdateView):
    '''
    View for logged in users to change their avatar
    '''
    model = Account
    template_name = 'account/avatar_change.html'
    form_class = ChangeAvatarForm

    def get_object(self, queryset=None):
        return self.request.user.account
    
    def get_success_url(self):
        '''
        Stay on the same page
        '''
        return self.request.path

def get_avatar(request, username):
    '''
    Returns the avatar for the given user
    '''
    try:
        username_validator(username)
    except ValidationError:
        raise Http404()

    account = get_object_or_404(Account, user__username=username)
    
    if not account.avatar:
        raise Http404('Avatar not found')

    with account.avatar.open('rb') as stream:
        content = stream.read()

    return HttpResponse(content, content_type="image/png")

class GenerateTokenView(LoginRequiredMixin, View):
    template_name = 'account/token.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        context = {
            'token': generate_token(self.request.user)
        }
        return render(request, self.template_name, context)

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'account/delete.html'
    success_url = '/account/logout/'

    def get_object(self, queryset=None):
        return self.request.user
