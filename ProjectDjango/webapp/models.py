from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from django.utils.translation import gettext_lazy as _


# Département model
class Departement(models.Model):
    nom_departement = models.CharField(
        max_length=250,
        verbose_name=_("Nom du département"),
        help_text=_("Entrez le nom du département"),
        validators=[MinLengthValidator(2)]
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Description détaillée du département")
    )

    def __str__(self):
        return self.nom_departement

    class Meta:
        verbose_name = _("Département")
        verbose_name_plural = _("Départements")
        ordering = ['nom_departement']


# Étudiant model
class Etudiant(models.Model):
    nom_etudiant = models.CharField(
        max_length=250,
        verbose_name=_("Nom"),
        help_text=_("Entrez le nom de l'étudiant"),
        validators=[MinLengthValidator(2)]
    )
    
    prenom_etudiant = models.CharField(
        max_length=250,
        verbose_name=_("Prénom"),
        help_text=_("Entrez le prénom de l'étudiant"),
        validators=[MinLengthValidator(2)]
    )
    
    date_naissance = models.DateField(
        verbose_name=_("Date de naissance"),
        help_text=_("Sélectionnez la date de naissance")
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email"),
        help_text=_("Entrez l'adresse email de l'étudiant"),
        validators=[EmailValidator()]
    )
    
    departement = models.ForeignKey(
        Departement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Département"),
        help_text=_("Sélectionnez le département de l'étudiant")
    )
    
    adresse = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Adresse"),
        help_text=_("Entrez l'adresse complète de l'étudiant")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de mise à jour")
    )

    def __str__(self):
        return f"{self.prenom_etudiant} {self.nom_etudiant}"

    class Meta:
        verbose_name = _("Étudiant")
        verbose_name_plural = _("Étudiants")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['nom_etudiant', 'prenom_etudiant']),
            models.Index(fields=['email']),
        ]  