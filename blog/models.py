from django.db import models
from django.conf import settings
from markdown import markdown
from mdeditor.fields import MDTextField
from django.dispatch import receiver
from django.shortcuts import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='blog')
    title = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modifiy = models.DateTimeField(auto_now=True)
    text = MDTextField("", blank=True)
    html_content = models.TextField('html content', blank=True)
    public_flag = models.IntegerField(default=1)  # 0 private  1 public
    published_flag = models.IntegerField(default=0)  # 0 草稿 1 已发表 2 垃圾箱

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog', args=(self.pk,))

    def delete_blog_completely(self):
        """完全删除blog，在数据库中删除"""
        self.delete()

    def move_to_trash(self):
        """删除blog，移动到回收箱"""
        self.published_flag = 2

    def publish(self):
        """发布 """
        self.published_flag = 1

    def draft(self):
        """从发布模式撤回 到 草稿模式"""
        self.published_flag = 0

    def set_private(self):
        """设置为私密，个人可见"""
        self.public_flag = 0

    def set_public(self):
        """设置为公开， 所有人可见"""
        self.public_flag = 1

    def can_be_collected(self):
        """发表， 公开状态的blog才能被收藏"""
        ret = False
        if self.public_flag == 1 and self.published_flag == 1:
            ret = True
        return ret

    def get_comment(self):
        """所有的评论"""
        return self.comment.all().order_by('-timestamp')

    def get_comment_num(self):
        return self.comment.all().count()

    def get_collected_num(self):
        """被收藏的数量"""
        return self.collect_blog.all().count()

    @staticmethod
    def get_all_public():
        return Blog.objects.filter(public_flag=1, published_flag=1).order_by('-last_modifiy')


class Collection(models.Model):
    """收藏"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             unique=False, related_name="collect_user")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
                             unique=False, related_name="collect_blog")
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """评论"""
    text = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               unique=False, related_name='user_comment')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
                             related_name='comment')
    timestamp = models.DateTimeField(auto_now_add=True)

# 只提交Markdown源文本，在服务器上进行转换
# instance 正要被保存的Blog对象实例
# update_fields 要更新的字段


@receiver(pre_save, sender=Blog)
def md_trans(sender, update_fields=None, instance=None, **kwargs):
    """在post文本提交时，进行markdown转html"""
    instance.html_content = markdown(instance.text, extensions=['markdown.extensions.extra', ])
    update_fields = ['html_content', ]

# @receiver(post_save, sender=Blog)
# def
