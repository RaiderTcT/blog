from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView, UpdateView, View, FormView
from django.views.generic import ListView, DetailView
from .forms import RegisterForm
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout
from .models import myUser
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator

# Create your views here.


class LoginView(auth_views.LoginView):
    template_name = 'login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'logged_out.html'


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_message = _("Account %(username)s was create successfully")

    def get_success_url(self):
        return reverse("users:login")


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'password_change.html'
    # success_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse("users:login")

    def form_valid(self, form):
        """
        修改密码后退出登录
        """
        response = super().form_valid(form)
        messages.success(self.request, _("Your password has been changed, please login again "))
        logout(self.request)
        return response


# class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
#     template_name = 'registration/password_change_done.html'
#     title = _('Password change successful')


class PasswordResetView(auth_views.PasswordResetView):
    from_email = settings.EMAIL_HOST_USER
    email_template_name = "password_reset_email.html"
    template_name = "password_reset.html"
    # subject_template_name =
    # success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        修改密码后退出登录
        """
        response = super().form_valid(form)
        reset_message = "We've emailed you instructions for setting your password,\
                        if an account exists with the email you entered.\
                        You should receive them shortly.\
                        If you don't receive an email,\
                        please make sure you've entered the address you registered with,\
                        and check your spam folder."

        messages.warning(self.request, _(reset_message))
        logout(self.request)
        return response

    def get_success_url(self):
        return reverse("blog:index")


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

    def get_success_url(self):
        return reverse("users:login")
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

    target_user = get_object_or_404(myUser, username=user_username)
    # user = request.user
    followed = target_user.followed.count()
    follower = target_user.follower.count()
    context = {'target_user': target_user, 'followed': followed,
               'follower': follower}
    if request.user.is_authenticated and request.user != target_user:
        follow_flag = False if request.user.is_following(target_user) else True
        followed_flag = True if target_user.is_following(request.user) else False
        context['follow_flag'] = follow_flag
        context['followed_flag'] = followed_flag

    return render(request, 'user.html', context)


class Profile(LoginRequiredMixin, UpdateView):
    model = myUser
    # form_class = ProfileForm
    fields = ['name', 'email', 'location', 'profession', 'bio', 'avatar']
    template_name = 'profile.html'

    def get_object(self):
        return self.model.objects.get(id=self.request.user.id)

    def get_login_url(self):
        return reverse('users:login')

    def get_success_url(self):
        return reverse("users:user", args=(self.request.user.username,))

# def edit_profile(request)


class FollowView(LoginRequiredMixin, ListView):
    model = myUser
    field = ['name', 'avatar', 'bio']
    paginate_by = 10
    paginate_orphans = 15

    def get_login_url(self):
        return reverse('users:login')


class FollowerView(FollowView):
    template_name = 'follower_list.html'
    context_object_name = 'follower_list'

    def get_queryset(self):
        self.target_user = get_object_or_404(self.model, username=self.kwargs['username'])
        return self.target_user.follower.filter().order_by('follower')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['target_user'] = self.target_user
        return context


class FollowedView(FollowView):
    template_name = 'followed_list.html'
    context_object_name = 'followed_list'

    def get_queryset(self):
        self.target_user = get_object_or_404(self.model, username=self.kwargs['username'])
        return self.target_user.followed.all().order_by("followed")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['target_user'] = self.target_user
        return context


@login_required
def follow(request, username):
    user = request.user
    target_user = get_object_or_404(myUser, username=username)
    if user.is_following(target_user):
        msg = _("You are already following this user !")
        messages.add_message(request, messages.ERROR, msg)
        return redirect(reverse('users:user', args=(user.username,)))
    user.follow(target_user)
    msg = _(f'You are following {username} !')
    messages.success(request, msg)
    return redirect(reverse('users:user', args=(user.username,)))


@login_required
def unfollow(request, username):
    user = request.user
    target_user = get_object_or_404(myUser, username=username)
    if not user.is_following(target_user):
        msg = _("You are not following this user!")
        messages.add_message(request, messages.ERROR, msg)
        return redirect(reverse('users:user', args=(user.username,)))
    user.unfollow(target_user)
    msg = _(f'You are not following {username} now !')
    messages.success(request, msg)
    return redirect(reverse('users:user', args=(user.username,)))
