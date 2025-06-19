# suivi/serializers.py
from rest_framework import serializers
from .models import DonneeSantee

class DonneeSanteeSerializer(serializers.ModelSerializer):
    imc = serializers.SerializerMethodField()

    class Meta:
        model = DonneeSantee
        fields = ['id', 'user', 'poids', 'taille', 'frequence_cardiaque', 'pression_arterielle', 'date_mesure', 'imc']

    def get_imc(self, obj):
        return obj.calcul_imc()