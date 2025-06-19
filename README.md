# Projet Santé 🩺

Application web Django pour le suivi des données de santé.

## Fonctions principales
- Authentification (Inscription + Connexion)
- Enregistrement des données : poids, IMC, etc.
- Analyse automatique (avec Pandas)
- Recommandations personnalisées
- Interface HTML simple (avec TailwindCSS)

## Stack
- Python / Django
- SQLite / PostgreSQL
- HTML / CSS / JavaScript
- Django REST Framework

## Lancer en local

```bash
git clone https://github.com/Stecy-Maeva/projet-sante.git
cd projet-sante

python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
