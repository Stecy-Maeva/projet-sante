# suivi/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie

import pandas as pd

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import DonneeSantee
from .serializers import DonneeSanteeSerializer

# ================================================
# ✅ API sécurisée (JWT Authentification)
# ================================================

class DonneeSanteeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = DonneeSantee.objects.all()
    serializer_class = DonneeSanteeSerializer

    def get_queryset(self):
        return DonneeSantee.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_analytics(request):
    qs = DonneeSantee.objects.filter(user=request.user)
    if not qs.exists():
        return JsonResponse({"message": "Pas encore de données"}, status=404)

    serializer = DonneeSanteeSerializer(qs, many=True)
    df = pd.DataFrame(serializer.data)

    avg_weight = df['poids'].mean()
    avg_bmi = df['imc'].mean()

    recommendations = []
    if avg_bmi > 25:
        recommendations.append("Votre IMC est élevé, pensez à revoir votre alimentation et votre activité physique.")
    elif avg_bmi < 18.5:
        recommendations.append("Votre IMC est bas, consultez un spécialiste pour ajuster votre régime.")
    else:
        recommendations.append("Votre IMC est bon, continuez à adopter un mode de vie sain.")

    return JsonResponse({
        "average_weight": avg_weight,
        "average_bmi": avg_bmi,
        "recommendations": recommendations
    }, status=200)


# ================================================
# ✅ Gestion des pages HTML (Application Web)
# ================================================

def home(request):
    return render(request, 'index.html')

@ensure_csrf_cookie
def register_page(request):
    return render(request, 'register.html')

@ensure_csrf_cookie
def login_page(request):
    return render(request, 'login.html')


# ✅ API d'inscription
@api_view(['POST'])
def api_register(request):
    try:
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"message": "Manque username ou password"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Nom d'utilisateur déjà pris"}, status=400)

        User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "Inscription OK"}, status=201)

    except Exception as e:
        return JsonResponse({"message": f"Erreur: {str(e)}"}, status=500)


# ✅ API de connexion
@api_view(['POST'])
def api_login(request):
    try:
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"message": "Manque username ou password"}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Connexion réussie"}, status=200)
        else:
            return JsonResponse({"message": "Identifiants invalides"}, status=401)

    except Exception as e:
        return JsonResponse({"message": f"Erreur serveur: {str(e)}"}, status=500)


# ================================================
# ✅ Système de suivi des données (Non sécurisé pour la démo)
# ================================================

def dashboard(request):
    donnees = DonneeSantee.objects.all()
    return render(request, "dashboard.html", {"donnees": donnees})


def ajouter_donnees(request):
    utilisateurs = User.objects.all()  # Récupérer tous les utilisateurs pour le formulaire

    if request.method == "POST":
        user_id = request.POST.get("user")
        poids = request.POST.get("poids")
        taille = request.POST.get("taille")
        frequence_cardiaque = request.POST.get("frequence_cardiaque")
        pression_arterielle = request.POST.get("pression_arterielle")

        if not poids or not taille:
            return JsonResponse({"message": "Poids et Taille sont obligatoires."}, status=400)

        try:
            poids = float(poids)
            taille = float(taille)
        except ValueError:
            return JsonResponse({"message": "Poids et Taille doivent être des nombres valides."}, status=400)

        # Détection automatique de l'utilisateur connecté OU sélection via formulaire
        user = User.objects.get(id=user_id) if user_id else request.user

        DonneeSantee.objects.create(
            user=user,
            poids=poids,
            taille=taille,
            frequence_cardiaque=frequence_cardiaque,
            pression_arterielle=pression_arterielle
        )

        return redirect("dashboard")

    return render(request, "ajouter.html", {"utilisateurs": utilisateurs})


def analyse_donnees(request):
    donnees = DonneeSantee.objects.all()
    if not donnees:
        return render(request, "dashboard.html", {"message": "Aucune donnée disponible"})

    df = pd.DataFrame(list(donnees.values()))
    avg_weight = df["poids"].mean()
    avg_bmi = (df["poids"] / (df["taille"] ** 2)).mean()

    recommendations = []
    if avg_bmi > 25:
        recommendations.append("Votre IMC est élevé, pensez à ajuster votre alimentation et votre activité physique.")
    elif avg_bmi < 18.5:
        recommendations.append("Votre IMC est bas, il est recommandé de consulter un spécialiste.")
    else:
        recommendations.append("Votre IMC est normal, continuez à maintenir une bonne hygiène de vie.")

    return render(request, "dashboard.html", {"avg_weight": avg_weight, "avg_bmi": avg_bmi, "recommendations": recommendations})