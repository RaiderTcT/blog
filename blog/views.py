from django.shortcuts import render

# Create your views here.


def index(request):
    context = {'name': 'Mystie'}
    return render(request, 'index.html', context)
