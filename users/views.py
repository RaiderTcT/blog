from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView, UpdateView, View, FormView
from django.views.generic import ListView, DetailView
from .forms import RegisterForm
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout, login
from .models import myUser
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from blog.models import Blog
from .tokens import token_generator
from .email import register_mail
from django.contrib.sites.shortcuts import get_current_site
from itsdangerous import SignatureExpired, BadPayload, BadSignature
# Create your views here.


class LoginView(auth_views.LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.has_confirmed:
            messages.add_message(self.request, settings.DANGER, _("用户未通过验证！请查收认证邮件并认证后再登录"))
        else:
            login(self.request, user)
        return redirect(self.get_success_url())


class LogoutView(auth_views.LogoutView):
    template_name = 'logged_out.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        token = token_generator.make_token(user.id)
        current_site = get_current_site(self.request)
        register_mail(token, user, recipient_list=[user.email, ],
                      use_https=False, current_site=current_site)
        messages.info(self.request, _('认证邮件已发送，请注意查收'))
        return response

    def get_success_url(self):
        return reverse("users:login")


def register_confirm(request, token):
    try:
        _id = token_generator.check_token(token)
    except BadPayload:
        messages.add_message(request, settings.DANGER, '验证错误,请重新注册')
    except BadSignature:
        messages.add_message(request, settings.DANGER, '验证错误,请重新注册')
    except SignatureExpired:
        _id = token_generator.remove_token(token)
        users = myUser.objects.filter(id=_id).all()
        for user in users:
            user.delete()
        messages.add_message(request, settings.DANGER, '验证码错误或已过期，请重新注册')
        return redirect(reverse('users:register'))

    try:
        user = myUser.objects.get(id=_id)
    except myUser.DoesNotExist:
        messages.add_message(request, settings.DANGER, '没有此用户，请重新注册')
        return redirect(reverse('users:register'))

    user.has_confirmed = True
    user.save()
    login(request, user)
    messages.add_message(request, messages.SUCCESS, "验证成功，已登录")

    return redirect(reverse('blog:index'))


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


class PasswordResetView(auth_views.PasswordResetView):
    from_email = settings.EMAIL_HOST_USER
    email_template_name = "email/password_reset_email.html"
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


def user(request, user_username):
    """查看个人信息"""

    target_user = get_object_or_404(myUser, username=user_username)
    # user = request.user
    followed = target_user.followed.count()
    follower = target_user.follower.count()
    blog_num = target_user.get_public_num()
    context = {'target_user': target_user, 'followed': followed,
               'follower': follower, 'blog_num': blog_num}
    if request.user.is_authenticated and request.user != target_user:
        follow_traget = True if request.user.is_following(target_user) else False
        target_follow = True if target_user.is_following(request.user) else False
        context['follow_traget'] = follow_traget
        context['target_follow'] = target_follow

    return render(request, 'user.html', context)


class Profile(LoginRequiredMixin, UpdateView):
    model = myUser
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
    else:
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
    else:
        user.unfollow(target_user)
        msg = _(f'You are not following {username} now !')
        messages.success(request, msg)
    return redirect(reverse('users:followed', args=(user.username,)))


@login_required
def collect(request, blog_id):
    user = request.user
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.can_be_collected() and blog.author != user:
        if user.is_collecting(blog):
            msg = _("You have already colleted this blog !")
            messages.add_message(request, messages.ERROR, msg)
        else:
            user.collect(blog)
    return redirect(reverse('blog:article', args=(blog_id,)))


@login_required
def uncollect(request, blog_id):
    user = request.user
    blog = get_object_or_404(Blog, id=blog_id)
    if not user.is_collecting(blog):
        msg = _("You are not collecting this blog")
        messages.error(request, msg)
    else:
        user.uncollect(blog)
    return redirect(reverse('blog:collection'))
