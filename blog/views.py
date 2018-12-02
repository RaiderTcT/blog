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
# Create your views here.

# url = reverse('users:login')


def index(request):

    context = {'name': 'Mystie'}
    url = reverse('users:login')
    print(url)
    # messages.add_message(request, "INFO", 'index')
    return render(request, 'index.html', context)


class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'text']
    label = {'title': "", 'text': ""}
    template_name = "mdeditor.html"

    def form_valid(self, form):
        """Blog的作者"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_login_url(self):
        return reverse('users:login')

    def get_success_url(self):
        return reverse("users:user", args=(self.request.user.username,))

    def get_context_data(self, **kwargs):
        """向模板中传递标题"""
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create Blog')
        return context


class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'text']
    template_name = "mdeditor.html"

    def form_valid(self, form):
        """Blog的作者"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_login_url(self):
        return reverse('users:login')

    def get_success_url(self):
        return reverse("users:user", args=(self.request.user.username,))

    def get_context_data(self, **kwargs):
        """向模板中传递标题"""
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Blog')
        return context

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


class BlogList(ListView):
    model = Blog
    fields = ['author', 'title']
    paginate_by = 10
    paginate_orphans = 15
    context_object_name = 'blog_list'
    template_name = 'blog_list.html'

    def get_queryset(self):
        self.article_user = get_object_or_404(myUser, username=self.kwargs['username'])
        queryset = Blog.objects.filter(author=self.article_user).order_by('-last_modifiy')
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['title'] = _(f"{self.article_user.username}'s Blog")
        return context
