from django.shortcuts import render, redirect
from .models import Predict
from .forms import PredictForm
from django.contrib.auth.decorators import login_required
import cgi

def home(request):
    context = {
        'predicts': Predict.objects.all()
    }
    return render(request, 'predictor/home.html', context)

def about(request):
    return render(request, 'predictor/about.html', {'title': 'About'})

def download(request):
    return render(request, 'predictor/download.html', {'title': 'Download'})

@login_required
def predict(request):
    return render(request, 'predictor/predict.html', {'title': 'Predict'})

@login_required
def result(request):
    if request.method == 'POST':
        form = PredictForm(request.POST)
        if form.is_valid():
           # predict_result = pred(form.summoner)
            return render(request, 'predictor/predict/result.html', {'form': form})
        else:
            redirect('predict.html')