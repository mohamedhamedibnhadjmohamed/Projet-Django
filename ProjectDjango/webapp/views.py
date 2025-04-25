from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, CreateEtudiantForm, UpdateEtudiantForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Etudiant, Departement
from django.db.models import Q
import logging
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied


def index(request):
    """Vue pour la page d'accueil"""
    return render(request, 'web/index.html')


# Enregistrement d'un nouvel utilisateur
def register(request):
    """Vue pour l'inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Inscription réussie. Vous pouvez maintenant vous connecter.'))
            return redirect('login')
        else:
            messages.error(request, _('Veuillez corriger les erreurs ci-dessous.'))

    context = {'form': form}
    return render(request, 'web/register.html', context)


# Connexion d'un utilisateur
def my_login(request):
    """Vue pour la connexion d'un utilisateur"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, _('Connexion réussie.'))
                return redirect('dashboard')
            else:
                messages.error(request, _('Nom d\'utilisateur ou mot de passe incorrect.'))
        else:
            messages.error(request, _('Veuillez corriger les erreurs ci-dessous.'))

    context = {'form': form}
    return render(request, 'web/login.html', context)


# Tableau de bord (liste des étudiants)
@login_required(login_url='login')
def dashboard(request):
    """Vue pour le tableau de bord (liste des étudiants)"""
    try:
        etudiants = Etudiant.objects.all().order_by('-created_at')
        departements = Departement.objects.all().order_by('nom_departement')
        context = {
            'etudiants': etudiants,
            'departements': departements
        }
        return render(request, 'web/dashboard.html', context)
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage du tableau de bord : {str(e)}")
        messages.error(request, _('Une erreur est survenue lors du chargement du tableau de bord.'))
        return redirect('login')


# Création d'un étudiant
@login_required(login_url='login')
def create_etudiant(request):
    """Vue pour la création d'un étudiant"""
    form = CreateEtudiantForm()

    if request.method == 'POST':
        form = CreateEtudiantForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('L\'étudiant a été créé avec succès.'))
                return redirect('dashboard')
            except Exception as e:
                logger.error(f"Erreur lors de la création de l'étudiant : {str(e)}")
                messages.error(request, _('Une erreur est survenue lors de la création de l\'étudiant.'))
        else:
            messages.error(request, _('Veuillez corriger les erreurs ci-dessous.'))

    context = {'form': form}
    return render(request, 'web/create-etudiant.html', context)


# Affichage des détails d'un étudiant
@login_required(login_url='login')
def view_etudiant(request, etudiant_id):
    """Vue pour l'affichage des détails d'un étudiant"""
    try:
        etudiant = get_object_or_404(Etudiant, id=etudiant_id)
        context = {'etudiant': etudiant}
        return render(request, 'web/view_etudiant.html', context)
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage de l'étudiant {etudiant_id} : {str(e)}")
        messages.error(request, _('Une erreur est survenue lors du chargement des détails de l\'étudiant.'))
        return redirect('dashboard')


# Mise à jour d'un étudiant
@login_required(login_url='login')
def update_etudiant(request, etudiant_id):
    """Vue pour la mise à jour d'un étudiant"""
    try:
        etudiant = get_object_or_404(Etudiant, id=etudiant_id)
        form = UpdateEtudiantForm(instance=etudiant)

        if request.method == 'POST':
            form = UpdateEtudiantForm(request.POST, instance=etudiant)
            if form.is_valid():
                form.save()
                messages.success(request, _('L\'étudiant a été mis à jour avec succès.'))
                return redirect('dashboard')
            else:
                messages.error(request, _('Veuillez corriger les erreurs ci-dessous.'))

        context = {'form': form, 'etudiant': etudiant}
        return render(request, 'web/update-etudiant.html', context)
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de l'étudiant {etudiant_id} : {str(e)}")
        messages.error(request, _('Une erreur est survenue lors de la mise à jour de l\'étudiant.'))
        return redirect('dashboard')


# Suppression d'un étudiant
@login_required(login_url='login')
def delete_etudiant(request, etudiant_id):
    """Vue pour la suppression d'un étudiant"""
    try:
        etudiant = get_object_or_404(Etudiant, id=etudiant_id)
        etudiant.delete()
        messages.success(request, _('L\'étudiant a été supprimé avec succès.'))
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'étudiant {etudiant_id} : {str(e)}")
        messages.error(request, _('Une erreur est survenue lors de la suppression de l\'étudiant.'))
    
    return redirect('dashboard')


# Recherche d'étudiants
logger = logging.getLogger(__name__)

@login_required(login_url='login')
def search(request):
    """Vue pour la recherche d'étudiants"""
    query = request.GET.get('query', '').strip()
    results = []

    try:
        if query:
            results = Etudiant.objects.filter(
                Q(nom_etudiant__icontains=query) |
                Q(prenom_etudiant__icontains=query) |
                Q(email__icontains=query)
            ).order_by('-created_at')
            
            if not results:
                messages.info(request, _('Aucun résultat trouvé pour votre recherche.'))
    except Exception as e:
        logger.error(f"Erreur lors de la recherche : {str(e)}")
        messages.error(request, _('Une erreur est survenue lors de la recherche.'))

    context = {'results': results, 'query': query}
    return render(request, 'web/search.html', context)


# Déconnexion d'un utilisateur
def my_logout(request):
    """Vue pour la déconnexion d'un utilisateur"""
    logout(request)
    messages.success(request, _('Déconnexion réussie.'))
    return redirect('login')


# Page 404 personnalisée
def custom_page_not_found(request, exception):
    """Vue pour la page 404 personnalisée"""
    return render(request, 'web/404.html', status=404)


@login_required(login_url='login')
def departements(request):
    try:
        departements = Departement.objects.all()
        return render(request, 'web/departements.html', {'departements': departements})
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des départements: {str(e)}")
        return redirect('dashboard')

@login_required(login_url='login')
def create_departement(request):
    if request.method == 'POST':
        try:
            nom_departement = request.POST.get('nom_departement')
            description = request.POST.get('description')
            
            if not nom_departement or not description:
                messages.error(request, "Tous les champs sont obligatoires")
                return redirect('create_departement')
            
            departement = Departement.objects.create(
                nom_departement=nom_departement,
                description=description
            )
            messages.success(request, "Département créé avec succès")
            return redirect('departements')
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du département: {str(e)}")
            return redirect('create_departement')
    
    return render(request, 'web/create_departement.html')

@login_required(login_url='login')
def view_departement(request, id):
    try:
        departement = Departement.objects.get(id=id)
        return render(request, 'web/view_departement.html', {'departement': departement})
    except Departement.DoesNotExist:
        messages.error(request, "Département non trouvé")
        return redirect('departements')
    except Exception as e:
        messages.error(request, f"Erreur lors de l'affichage du département: {str(e)}")
        return redirect('departements')

@login_required(login_url='login')
def update_departement(request, id):
    try:
        departement = Departement.objects.get(id=id)
        
        if request.method == 'POST':
            nom_departement = request.POST.get('nom_departement')
            description = request.POST.get('description')
            
            if not nom_departement or not description:
                messages.error(request, "Tous les champs sont obligatoires")
                return redirect('update_departement', id=id)
            
            departement.nom_departement = nom_departement
            departement.description = description
            departement.save()
            
            messages.success(request, "Département mis à jour avec succès")
            return redirect('departements')
        
        return render(request, 'web/create_departement.html', {'departement': departement})
    except Departement.DoesNotExist:
        messages.error(request, "Département non trouvé")
        return redirect('departements')
    except Exception as e:
        messages.error(request, f"Erreur lors de la mise à jour du département: {str(e)}")
        return redirect('departements')

@login_required(login_url='login')
def delete_departement(request, id):
    try:
        departement = Departement.objects.get(id=id)
        
        # Vérifier s'il y a des étudiants dans ce département
        if departement.etudiant_set.exists():
            messages.error(request, "Impossible de supprimer ce département car il contient des étudiants")
            return redirect('departements')
        
        departement.delete()
        messages.success(request, "Département supprimé avec succès")
        return redirect('departements')
    except Departement.DoesNotExist:
        messages.error(request, "Département non trouvé")
        return redirect('departements')
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression du département: {str(e)}")
        return redirect('departements')

@login_required(login_url='login')
def search_departement(request):
    """Vue pour la recherche de départements"""
    query = request.GET.get('query', '').strip()
    results = []

    try:
        if query:
            results = Departement.objects.filter(
                Q(nom_departement__icontains=query) |
                Q(description__icontains=query)
            ).order_by('nom_departement')
            
            if not results:
                messages.info(request, _('Aucun résultat trouvé pour votre recherche.'))
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de départements : {str(e)}")
        messages.error(request, _('Une erreur est survenue lors de la recherche.'))

    context = {'results': results, 'query': query}
    return render(request, 'web/search_departement.html', context)

@login_required(login_url='login')
def etudiants(request):
    """Vue pour la gestion des étudiants"""
    try:
        etudiants = Etudiant.objects.all().order_by('-created_at')
        context = {'etudiants': etudiants}
        return render(request, 'web/etudiants.html', context)
    except Exception as e:
        logger.error(f"Erreur lors du chargement des étudiants : {str(e)}")
        messages.error(request, _('Une erreur est survenue lors du chargement des étudiants.'))
        return redirect('dashboard')

def privacy(request):
    """Vue pour la page de politique de confidentialité"""
    return render(request, 'web/privacy.html')