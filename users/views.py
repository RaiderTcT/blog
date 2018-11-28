from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView, UpdateView, View, FormView
from .forms import RegisterForm
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout
from .models import myUser
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.


class LoginView(auth_views.LoginView):
    template_name = 'login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'index.html'


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    # 不在函数无法调用reverse
    success_url = reverse_lazy('login')
    success_message = _("Account %(username)s was create successfully")


class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Your password has been changed, please login again "))
        logout(self.request)
        return response


class PasswordResetView(auth_views.PasswordResetView):
    from_email = settings.EMAIL_HOST_USER
    email_template_name = "password_reset_email.html"
    template_name = "password_reset.html"
    # subject_template_name =
    success_url = reverse_lazy('users:login')


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    # success_url = 'account/login'
    template_name = 'password_reset_confirm.html'


# @login_required
# def change_password(request):
#     if request.method == "POST":
#         form = PasswordChangeForm(request.POST)
#         if form.is_valid():
#             user = request.user
#             if check_password(request.POST['old_password'], user.password):
#                 user.password = make_password(request.POST['password1'])
#                 user.save()
#                 return redirect('users:login')
#     else:
#         form = PasswordChangeForm(user=request.user)
#     context = {'form': form}
#     return render(request, 'password_change.html', context)


def user(request, user_username):
    """查看个人信息"""
    if request.method == "GET":
        target_user = get_object_or_404(myUser, username=user_username)
        # user = request.user
        context = {'target_user': target_user}
    return render(request, 'user.html', context)


class Profile(LoginRequiredMixin, UpdateView):
    model = myUser
    # form_class = ProfileForm
    fields = ['name', 'email', 'location', 'profession', 'bio', 'avatar']
    template_name = 'profile.html'

# def edit_profile(request)
