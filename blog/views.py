from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
# Create your views here.


def index(request):

    context = {'name': 'Mystie'}
    # messages.add_message(request, "INFO", 'index')
    messages.success(request, 'success')
    messages.error(request, 'error')
    return render(request, 'index.html', context)
