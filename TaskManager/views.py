from django.shortcuts import render
from tasks.models import Task


def home(request, categorySlug=None):
    data = Task.objects.all()
    return render(request, 'home.html', {'data': data})