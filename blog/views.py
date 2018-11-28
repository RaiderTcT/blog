from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
# Create your views here.

# url = reverse('users:login')


def index(request):

    context = {'name': 'Mystie'}
    url = reverse('users:login')
    print(url)
    # messages.add_message(request, "INFO", 'index')
    return render(request, 'index.html', context)
