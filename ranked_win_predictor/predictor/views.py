from django.shortcuts import render
# Create your views here.
predicts = [
    {
        'summoner': 'JimmyyW', #httpPOST summonername used as parameter for functionality
        'predict': 'blue', #result from neural net
        'result': 'correct', #validation on the above
        'date': 'April 04, 2019', #logged date of instance
        'confidence': '88'
    },
    {
        'summoner': 'stozer',
        'predict': 'blue',
        'result': 'incorrect',
        'date': 'April 04, 2019',
        'confidence': '80'
    }
]

def home(request):
    context = {
        'predicts': predicts
    }
    return render(request, 'predictor/home.html', context)

def about(request):
    return render(request, 'predictor/about.html', {'title': 'About'})

def download(request):
    return render(request, 'predictor/download.html', {'title': 'Download'})

