from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Blog
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from users.models import myUser
from django.contrib.auth.decorators import login_required
# Create your views here.

# url = reverse('users:login')


class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'text']
    label = {'title': "", 'text': ""}
    template_name = "create_blog.html"

    def form_valid(self, form):
        """Blog的作者"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_login_url(self):
        return reverse('users:login')

    def get_success_url(self):
        return reverse("blog:post-list")

    # def get_context_data(self, **kwargs):
    #     """向模板中传递标题"""
    #     context = super().get_context_data(**kwargs)
    #     context['web_title'] = _('Create Blog')
    #     context['create'] = 1
    #     return context


class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'text']
    label = {'title': "", 'text': ""}
    template_name = "update_blog.html"

    def form_valid(self, form):
        """Blog的作者"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_login_url(self):
        return reverse('users:login')

    def get_success_url(self):
        return reverse("blog:article", args=(self.get_object().id,))

    # def get_context_data(self, **kwargs):
    #     """向模板中传递标题"""
    #     context = super().get_context_data(**kwargs)
    #     context['web_title'] = _('Edit Blog')
    #     context['create'] = 0
    #     return context

    def get(self, request, *args, **kwargs):
        """ 尝试修改他人的blog时，重定向创建新Blog
            随意填写blog的id， 也会重定向到创建新Blog
        """
        try:
            self.object = self.get_object()
        except Http404:
            return redirect(reverse('blog:blog-add'))

        if request.user != self.object.author:
            response = redirect(reverse('blog:blog-add'))
        else:
            response = super().get(request, *args, **kwargs)

        return response


class Article(DetailView):
    model = Blog
    fields = ['title', 'html_content', 'author']
    context_object_name = 'article'
    template_name = 'article.html'

    def get_object(self):
        obj = get_object_or_404(self.model, id=self.kwargs['article_id'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            collected = user.is_collecting(self.object)
            context['collected'] = collected
        return context


class BlogListView(ListView):
    paginate_by = 7
    paginate_orphans = 0
    context_object_name = 'blog_list'


class UserBlogListView(BlogListView):
    template_name = 'blog_list.html'

    def get_queryset(self):
        self.article_user = get_object_or_404(myUser, username=self.kwargs['username'])
        queryset = Blog.objects.filter(author=self.article_user).order_by('-last_modifiy')
        queryset = queryset.filter(published_flag=1, public_flag=1)
        return queryset

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['title'] = _(f"{self.article_user.username}'s Blogs")
        context['target_user'] = self.article_user
        return context


class IndexView(BlogListView):
    template_name = 'index.html'

    def get_queryset(self):
        """获取所有公开的文章"""
        queryset = Blog.objects.filter(published_flag=1).order_by('-last_modifiy')
        return queryset


class CollectionListView(LoginRequiredMixin, BlogListView):
    template_name = "collection.html"

    def get_login_url(self):
        return reverse('users:login')

    def get_queryset(self):
        user = self.request.user
        return user.collection()


class PostListView(LoginRequiredMixin, BlogListView):
    template_name = 'post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['private_num'] = self.request.user.get_private_num()
        context['public_num'] = self.request.user.get_public_num()
        context['draft_num'] = self.request.user.get_draft_num()
        context['trash_num'] = self.request.user.get_trash_num()
        context['all_num'] = self.request.user.get_all_num()
        return context


class PostListAllView(PostListView):

    def get_queryset(self):
        user = self.request.user
        queryset = user.get_all()
        return queryset


class PostListPublicView(PostListView):

    def get_queryset(self):
        queryset = self.request.user.get_public()
        return queryset


class PostListPrivateView(PostListView):

    def get_queryset(self):
        queryset = self.request.user.get_private()
        return queryset


class PostListDraftView(PostListView):

    def get_queryset(self):
        queryset = self.request.user.get_draft()
        return queryset


class PostListTrashView(PostListView):

    def get_queryset(self):
        queryset = self.request.user.get_trash()
        return queryset


@login_required
def post_public(request, id):
    """发布， 公开模式"""
    blog = get_object_or_404(Blog, id=id, author=request.user)
    blog.publish()
    blog.set_public()
    blog.save()
    return redirect(reverse('blog:postlist-public'))


@login_required
def post_private(request, id):
    """发布， 公开模式"""
    blog = get_object_or_404(Blog, id=id, author=request.user)
    blog.publish()
    blog.set_private()
    blog.save()
    return redirect(reverse('blog:postlist-private'))


@login_required
def cancel(request, id):
    """撤回"""
    blog = get_object_or_404(Blog, id=id, author=request.user)
    blog.draft()
    blog.save()
    return redirect(reverse('blog:postlist-draft'))


@login_required
def move_to_trash(request, id):
    """移除到垃圾箱"""
    blog = get_object_or_404(Blog, id=id, author=request.user)
    blog.move_to_trash()
    blog.save()
    return redirect(reverse('blog:postlist-trash'))


@login_required
def recover(request, id):
    """从垃圾箱回收到草稿箱"""
    blog = get_object_or_404(Blog, id=id, author=request.user)
    blog.draft()
    blog.save()
    return redirect(reverse('blog:postlist-draft'))


@login_required
def delete_blog_completely(request, id):
    """从数据库中删除"""
    blog = get_object_or_404(Blog, id=id, author=request.user)
    blog.delete_blog_completely()
    return redirect(reverse('blog:postlist'))
