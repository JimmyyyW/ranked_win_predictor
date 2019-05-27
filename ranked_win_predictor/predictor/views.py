from django.shortcuts import render
from .models import Predict

def home(request):
    context = {
        'predicts': Predict.objects.all()
    }
    return render(request, 'predictor/home.html', context)

def about(request):
    return render(request, 'predictor/about.html', {'title': 'About'})

def download(request):
    return render(request, 'predictor/download.html', {'title': 'Download'})

