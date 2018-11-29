from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.conf import settings
# Create your models here.


class Follow(models.Model):
    """
        followed 被关注者
        follower 粉丝
    """
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='followed', unique=False)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='follower', unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"followed:{self.followed}, fans:{self.follower}"


class myUser(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    location = models.CharField(_("Location"), max_length=50, blank=True)
    name = models.CharField(_('Name'), max_length=20, blank=True)
    bio = models.TextField(_('Tell us a little bit about yourself'), blank=True)
    profession = models.CharField(_("Profession"), max_length=20, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatar/%Y/%m/%d',
                               default='avatar/wenhuang.jpg', blank=True, null=True)
    # follower = models.ForeignKey('self', on_delete=models.CASCADE,
    #                              related_name='follower_user', blank=True, default='self')
    # following = models.ForeignKey('self', on_delete=models.CASCADE,
    #                               related_name='following_user', blank=True, default='self')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:user', args=(self.username,))

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            f.save()

    def unfollow(self, user):
        f = self.followed.filter(followed=user).first()
        if f:
            f.delete()

    def is_followed_by(self, user):
        if user is None:
            return False
        else:
            return self.follower.filter(follower=user).first() is not None

    def is_following(self, user):
        if user is None:
            return False
        else:
            return self.followed.filter(followed=user).first() is not None
