from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
# Create your models here.


# class Follow(models.Model):
#     fan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     idol = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)


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

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:user', args=(self.username,))
