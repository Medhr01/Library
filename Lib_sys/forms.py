from django import forms
from .models import *
from django.core.validators import MaxLengthValidator

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom',  'prenom', 'date_de_naissance', 'CNI']
        widgets = { 'nom': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'prenom': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'date_de_naissance': forms.DateInput(attrs={'type':'date', 'class':"form-control" ,'id':"floatingInput"}),
                    'CNI': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),}
class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['Exemplaire', 'Client', 'Date_retourn', 'mUser']

class livre_f(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre','auteur','description','ISBN','langue','quantite']
        widgets = { 'titre': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'auteur': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'description': forms.Textarea(attrs={'style': "height:150px;",'class':"form-control" ,'id':"floatingInput"}),
                    'ISBN': forms.TextInput(attrs={'class':"form-control" ,'id':"floatingInput"}),
                    'langue': forms.Select(choices=Livre.LANGUE_CHOICES, attrs={'class':"form-select" ,'id':"floatingInput"}),
                    'quantite': forms.NumberInput(attrs={'min': Livre.number_exemplaires , 'class':"form-control" ,'id':"floatingInput"})
                    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ISBN'].validators.append(MaxLengthValidator(13))
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)