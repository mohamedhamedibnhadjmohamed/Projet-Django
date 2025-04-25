from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import handler404

handler404 = 'webapp.views.custom_page_not_found'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.my_logout, name='logout'),

    path('etudiant/create/', views.create_etudiant, name='create_etudiant'),
    path('etudiant/<int:etudiant_id>/', views.view_etudiant, name='view_etudiant'),
    path('etudiant/<int:etudiant_id>/update/', views.update_etudiant, name='update_etudiant'),
    path('etudiant/<int:etudiant_id>/delete/', views.delete_etudiant, name='delete_etudiant'),
    path('search/', views.search, name='search'),

    path('departements/', views.departements, name='departements'),
    path('departements/create/', views.create_departement, name='create_departement'),
    path('departements/<int:id>/', views.view_departement, name='view_departement'),
    path('departements/<int:id>/update/', views.update_departement, name='update_departement'),
    path('departements/<int:id>/delete/', views.delete_departement, name='delete_departement'),
]