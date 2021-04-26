from django.shortcuts import render, redirect
from django.http import Http404


# Create your views here.
def index(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'dogs/index.html')