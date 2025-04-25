from django.core.management.base import BaseCommand
from webapp.models import Departement


class Command(BaseCommand):
    help = 'Crée un département par défaut'

    def handle(self, *args, **options):
        if not Departement.objects.exists():
            Departement.objects.create(
                nom_departement="Informatique",
                description="Département d'informatique"
            )
            self.stdout.write(self.style.SUCCESS('Département par défaut créé avec succès'))
        else:
            self.stdout.write(self.style.SUCCESS('Des départements existent déjà')) 