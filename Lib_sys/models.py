from typing import Iterable
from django.db import models
from datetime import *

import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
# Create your models here.

class mUser(AbstractUser):
    Identifient= models.CharField(max_length=20, unique=True, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.Identifient:
            r = str(uuid.uuid4().int)[:6]
            self.Identifient = 'ADM' + r
        super().save(*args, **kwargs)



class Livre(models.Model):
    LANGUE_CHOICES = [
        ('', 'Select langue'),
        ('AR','Arabe'),
        ('FR', 'Français'),
        ('EN', 'Anglais'),
        ('ES', 'Espagnol'),
        ('AUTRE', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('Disponible pour prêt', 'Disponible'),
        ('Hors prêt', 'Hors prêt')
    ]
    titre = models.CharField(max_length=100)
    auteur = models.CharField(max_length=100)
    description = models.TextField()
    ISBN = models.CharField(max_length=13, unique=True)
    langue = models.CharField(max_length=6, choices=LANGUE_CHOICES)
    number_exemplaires = models.PositiveBigIntegerField(default=0)
    quantite = models.PositiveIntegerField(default=0)
    statut = models.CharField(max_length=50, default="Disponible pour prêt", choices=STATUT_CHOICES)
    cover = models.ImageField(upload_to="livre/")
    
    def __str__(self):
        return f"{self.titre}"
    def save(self, *args, **kwargs):
     
        super().save(*args, **kwargs)


    def prett(self, act):
        if act == "oui":
            self.statut = "Disponible pour prêt"
        else:
            self.statut = "Hors prêt"

        self.save()

    
    

class Client(models.Model):
    STATUT_CHOICES = [
        ('Active', 'Active'),
        ('Non active', 'Non active'),
        ('Banned', 'Banned'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    CNI = models.CharField(max_length=20)
    date_d_inscription = models.DateField(auto_now_add=True)
    date_validite = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="clients/")
    statut = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return f'{self.nom} {self.prenom}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_d_inscription = datetime.now().date() 
            self.date_validite = self.date_d_inscription + timedelta(days=365)
            
        super().save(*args, **kwargs)

    def activer(self):
        self.statut ="Active"
        self.save()
    def desactiver(self):
        self.statut ="Non active"
        self.save()

    

    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
 
class Exemplaire(models.Model):
    STATUT_CHOICES = [('Disponible', 'Disponible'),
                    ('Perdu', 'Perdu'),
                    ('Endommagé', 'Endommagé'),
                    ('Prêté', 'Prêté')]
    livre = models.ForeignKey('Livre', on_delete=models.CASCADE)
    numero_exemplaire = models.CharField(max_length=100)
    statut = models.CharField(max_length=50, default='Disponible')


    def __str__(self):
        return f"<b>{self.livre.titre}</b> / {self.numero_exemplaire}"
    
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def emprunt_exmp(self):
        self.statut = 'Prêté'
        self.save()

    def renouvler(self):
        self.statut = 'Disponible'
        self.save()

    def retirer(self):
        self.delete()
    
    


    def perdu(self):
        self.statut = "Perdu"
        self.save()


    




@receiver(post_save, sender=Exemplaire)
@receiver(post_delete, sender=Exemplaire)
def auto_update_number_exemplaires(sender, instance, **kwargs):
        livre = instance.livre
        dispo_exmp = Exemplaire.objects.filter(livre=livre, statut='Disponible').count()
        livre.number_exemplaires = dispo_exmp
        livre.save()


@receiver(post_save, sender=Livre)
def auto_create_exemplaires(sender, instance, created, **kwargs):
    if created:
            for i in range(instance.quantite):
                Exemplaire.objects.create(
                            livre=instance,
                            numero_exemplaire=f"{instance.ISBN}-{i + 1}",
                            statut='Disponible'
                        )
            

class Emprunt(models.Model):
    Exemplaire = models.ForeignKey('Exemplaire', on_delete=models.CASCADE)
    Client = models.ForeignKey('Client', on_delete=models.CASCADE)
    mUser = models.ForeignKey('mUser', on_delete=models.CASCADE)
    Date_emprunt = models.DateField(auto_now_add=True)
    Date_retourn =  models.DateField()
    Date_retourne = models.DateField(null=True, blank=True)

    def return_exmp(self, etat):
        if etat == "v":
            self.Exemplaire.statut = 'Disponible'
        else:
            self.Exemplaire.statut = 'Endommagé'
        self.Exemplaire.save()
        self.Date_retourne = datetime.today()
        self.save()
    






    


    



