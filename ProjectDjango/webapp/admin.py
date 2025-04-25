from django.contrib import admin
from .models import * 


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    pass

@admin.register(Etudiant)
class EtudianteAdmin(admin.ModelAdmin):
    pass