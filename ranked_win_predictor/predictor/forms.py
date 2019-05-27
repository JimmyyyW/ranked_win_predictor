from django import forms

class PredictForm(forms.Form):
    summoner = forms.CharField(label = 'summoner', max_length=15)