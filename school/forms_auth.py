from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Obligatoire. Entrez une adresse email valide.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Obligatoire.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Obligatoire.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Obligatoire. 150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement.'
        self.fields['password1'].help_text = 'Obligatoire. Au moins 8 caractères.'
        self.fields['password2'].help_text = 'Entrez le même mot de passe pour validation.'
        
        # Labels en français
        self.fields['username'].label = 'Nom d\'utilisateur'
        self.fields['first_name'].label = 'Prénom'
        self.fields['last_name'].label = 'Nom'
        self.fields['email'].label = 'Adresse email'
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmer le mot de passe'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
