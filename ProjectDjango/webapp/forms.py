from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput, EmailInput, DateInput
from django.utils.translation import gettext_lazy as _
from .models import Etudiant, Departement


# Formulaire d'inscription utilisateur
class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Nom d\'utilisateur')
        }),
        help_text=_('150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement.')
    )
    
    password1 = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Mot de passe')
        }),
        help_text=_(
            'Votre mot de passe doit contenir au moins 8 caractères et ne peut pas être entièrement numérique.'
        )
    )
    
    password2 = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirmation du mot de passe')
        }),
        help_text=_('Entrez le même mot de passe que précédemment, pour vérification.')
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# Formulaire de connexion utilisateur
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Nom d\'utilisateur')
        })
    )
    
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Mot de passe')
        })
    )


# Formulaire de création d'un étudiant
class CreateEtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            'nom_etudiant', 
            'prenom_etudiant', 
            'date_naissance', 
            'email', 
            'departement', 
            'adresse'
        ]
        widgets = {
            'nom_etudiant': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nom'),
                'minlength': '2'
            }),
            'prenom_etudiant': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Prénom'),
                'minlength': '2'
            }),
            'date_naissance': DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Email')
            }),
            'adresse': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Adresse')
            }),
            'departement': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        empty_label=_("Sélectionnez un département"),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def clean_nom_etudiant(self):
        nom = self.cleaned_data.get('nom_etudiant')
        if len(nom) < 2:
            raise forms.ValidationError(_("Le nom doit contenir au moins 2 caractères."))
        return nom

    def clean_prenom_etudiant(self):
        prenom = self.cleaned_data.get('prenom_etudiant')
        if len(prenom) < 2:
            raise forms.ValidationError(_("Le prénom doit contenir au moins 2 caractères."))
        return prenom


# Formulaire de mise à jour d'un étudiant
class UpdateEtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            'nom_etudiant', 
            'prenom_etudiant', 
            'date_naissance', 
            'email', 
            'departement', 
            'adresse'
        ]
        widgets = {
            'nom_etudiant': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nom'),
                'minlength': '2'
            }),
            'prenom_etudiant': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Prénom'),
                'minlength': '2'
            }),
            'date_naissance': DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Email')
            }),
            'adresse': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Adresse')
            }),
        }

    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        empty_label=_("Sélectionnez un département"),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def clean_nom_etudiant(self):
        nom = self.cleaned_data.get('nom_etudiant')
        if len(nom) < 2:
            raise forms.ValidationError(_("Le nom doit contenir au moins 2 caractères."))
        return nom

    def clean_prenom_etudiant(self):
        prenom = self.cleaned_data.get('prenom_etudiant')
        if len(prenom) < 2:
            raise forms.ValidationError(_("Le prénom doit contenir au moins 2 caractères."))
        return prenom