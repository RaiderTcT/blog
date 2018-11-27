from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView as BaseLoginView, \
    LogoutView as BaseLogoutView
from django.views.generic.edit import CreateView, UpdateView, View, FormView
from .forms import RegisterForm
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from .models import myUser
# Create your views here.


class LoginView(BaseLoginView):
    template_name = 'login.html'


class LogoutView(BaseLogoutView):
    template_name = 'index.html'


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/'
    success_message = _("%(username)s was create successfully")


def user(request, user_username):
    """查看个人信息"""
    target_user = get_object_or_404(myUser, username=user_username)
    # user = request.user
    context = {'target_user': target_user}
    return render(request, 'user.html', context)
