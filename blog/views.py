from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .models import Blog
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
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
    template_name = "mdeditor.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_login_url(self):
        return reverse('users:login')

    def get_success_url(self):
        return reverse("users:user", args=(self.request.user.username,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create Blog')
        return context


class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'text']
    template_name = "mdeditor.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_login_url(self):
        return reverse('users:login')

    def get_success_url(self):
        return reverse("users:user", args=(self.request.user.username,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Blog')
        return context
    # def get_object(self):
    #     obj = super().get_object()
    #     user = self.request.user
    #     if obj.author != user:
    #         return redirect(reverse('blog:blog-add'))
    #     else:
    #         return obj


# class BlogDelete(LoginRequiredMixin, DeleteView):
#     model = Blog
#     fields = ['title', 'text']
#     template_name = "mdeditor.html"

#     def get_login_url(self):
#         return reverse('users:login')

#     def get_success_url(self):
#         return reverse("users:user", args=(self.request.user.username,))
