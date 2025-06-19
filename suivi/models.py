# suivi/models.py

from django.db import models
from django.contrib.auth.models import User

class DonneeSantee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Ajout de `null=True` pour éviter l'erreur de migration
    poids = models.FloatField()
    taille = models.FloatField()
    frequence_cardiaque = models.IntegerField()
    pression_arterielle = models.CharField(max_length=20)
    date_mesure = models.DateTimeField(auto_now_add=True)

    def calcul_imc(self):
        if self.taille:
            return round(self.poids / (self.taille ** 2), 2)
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} – {self.date_mesure.strftime('%Y-%m-%d %H:%M')}"