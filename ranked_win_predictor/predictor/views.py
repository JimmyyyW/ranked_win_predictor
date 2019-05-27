from django.shortcuts import render, redirect
from .models import Predict
from .forms import PredictForm
from django.contrib.auth.decorators import login_required
from ranked_predictor_temp.predict import predict as pred
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
            #x = 1
            x = form.cleaned_data['summoner']
            nnr = pred(x)
            if nnr[0] == 0:
                nnr = 'RED'
            elif nnr[0] == 1:
                nnr = 'BLUE'
            else:
                nnr = 'ERROR'
            return render(request, 'predictor/predict/result.html', {'form': nnr})
        else:
            redirect('predict.html')