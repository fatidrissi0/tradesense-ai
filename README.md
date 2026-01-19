🚀 TradeSense AI
Plateforme de trading virtuel avec analyse AI en temps réel

Une application full-stack permettant aux utilisateurs de pratiquer le trading avec de l'argent virtuel, recevoir des signaux de trading générés par IA, et participer à des défis mensuels avec classement.

🌐 Démo en ligne

Application Frontend: https://tradesense-d7rb9lqnp-fatima-zahra-reghini-idrissis-projects.vercel.app
API Backend: https://fatimazahra2.pythonanywhere.com


📋 Table des matières
Fonctionnalités 
Technologies utilisées
Architecture
Installation locale
Déploiement
Structure du projet
API Endpoints

✨ Fonctionnalités

Pour les utilisateurs

🔐 Authentification sécurisée (JWT)  
💰 Trading virtuel avec capital initial de 10,000 MAD      
📊 Données de marché en temps réel (actions internationales et Bourse de Casablanca)    
🤖 Signaux de trading AI basés sur analyse technique     
🏆 Classement mensuel avec récompenses        
💳 Plans d'abonnement (Free, Pro, Premium)             
📈 Historique des transactions          
📉 Graphiques interactifs des prix        

Fonctionnalités techniques

Architecture REST API
Base de données relationnelle (SQLite/PostgreSQL)
Authentification par tokens JWT
CORS configuré pour sécurité cross-origin
Responsive design (mobile-friendly)

🛠 Technologies utilisées

Frontend
React (avec TypeScript)
Vite - Build tool moderne et rapide
Tailwind CSS - Styling utility-first
Recharts - Visualisation de données
Axios - Requêtes HTTP
Lucide React - Icônes modernes

Backend
Flask (Python) - Framework web léger
Flask-JWT-Extended - Gestion JWT
Flask-CORS - Gestion Cross-Origin
SQLAlchemy - ORM pour base de données
Bcrypt - Hachage de mots de passe
Python-dotenv - Variables d'environnement

Déploiement
Frontend: Vercel
Backend: PythonAnywhere
Version Control: GitHub


🏗 Architecture
┌─────────────┐         HTTPS          ┌──────────────┐
│   Frontend  │ ◄──────────────────► │   Backend    │
│   (Vercel)  │      REST API         │(PythonAnywhere)│
│   React+TS  │                       │    Flask     │
└─────────────┘                       └──────┬───────┘
                                             │
                                             ▼
                                      ┌──────────────┐
                                      │   Database   │
                                      │   SQLite     │
                                      └──────────────┘

💻 Installation locale
Prérequis
Python 3.11+
Node.js 18+
Git

1. Cloner le repository
bash
git clone https://github.com/fatidrissi0/tradesense-ai.git
cd tradesense-ai

2. Configuration Backend
bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate
# Ou sur Mac/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
echo SECRET_KEY=votre_secret_key > .env
echo JWT_SECRET_KEY=votre_jwt_secret >> .env
echo FLASK_ENV=development >> .env
echo SQLALCHEMY_DATABASE_URI=sqlite:///tradesense.db >> .env

# Lancer le serveur
python app.py
Le backend sera accessible sur http://127.0.0.1:5000

3. Configuration Frontend
bash
# Ouvrir un nouveau terminal
cd frontend

# Installer les dépendances
npm install

# Créer le fichier .env
echo VITE_API_URL=http://127.0.0.1:5000 > .env

# Lancer le serveur de développement
npm run dev
Le frontend sera accessible sur http://localhost:5173

4. Tester l'application
Ouvrez http://localhost:5173 dans votre navigateur
Créez un compte
Commencez à trader!
🚀 Déploiement
Backend - PythonAnywhere
Note sur le choix de la plateforme: PythonAnywhere a été choisi comme alternative à Render et Railway, car ces derniers nécessitent une carte bancaire pour l'utilisation de leurs plans gratuits, ce qui n'était pas accessible pour ce projet étudiant.

Étapes de déploiement:
Créer un compte sur PythonAnywhere
Cloner le repository:
bash
git clone https://github.com/fatidrissi0/tradesense-ai.git
cd tradesense-ai
Créer un virtualenv:
bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configurer les variables d'environnement: Créer un fichier .env:
env
SECRET_KEY=<secret_key_production>
JWT_SECRET_KEY=<jwt_secret_production>
FLASK_ENV=production
SQLALCHEMY_DATABASE_URI=sqlite:////tmp/tradesense.db
Configurer WSGI: Dans le fichier WSGI de PythonAnywhere:
python
import sys
import os

path = '/home/<username>/tradesense-ai'
if path not in sys.path:
    sys.path.append(path)

os.environ['FLASK_ENV'] = 'production'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tradesense.db'

from app import app as application
Reload l'application dans le dashboard Web
Frontend - Vercel
Connecter le repository GitHub à Vercel
Configurer les paramètres:
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Ajouter la variable d'environnement:
VITE_API_URL = https://<votre-username>.pythonanywhere.com
Déployer - Vercel déploie automatiquement à chaque push sur main


📁 Structure du projet
tradesense-ai/
├── backend/
│   ├── routes/              # Endpoints API
│   │   ├── auth.py          # Authentication
│   │   ├── trading.py       # Trading operations
│   │   ├── payment.py       # Subscriptions
│   │   ├── leaderboard.py   # Rankings
│   │   ├── market.py        # Market data
│   │   └── signals.py       # AI signals
│   ├── app.py               # Application principale
│   ├── models.py            # Modèles SQLAlchemy
│   ├── config.py            # Configuration
│   └── requirements.txt     # Dépendances Python
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Composants React
│   │   ├── pages/           # Pages de l'app
│   │   ├── services/        # API calls
│   │   ├── api.ts           # Configuration Axios
│   │   └── App.tsx          # App principale
│   ├── package.json
│   └── vite.config.ts
│
├── .gitignore
└── README.md


🔌 API Endpoints
Authentication
POST   /api/auth/register    # Inscription
POST   /api/auth/login       # Connexion
GET    /api/auth/me          # Profil utilisateur (JWT requis)
Trading
GET    /api/trades/history        # Historique des trades (JWT)
POST   /api/trades/execute        # Exécuter un trade (JWT)
GET    /api/challenges/active     # Défi actif (JWT)
Market Data
GET    /api/market/live/:symbol      # Prix en temps réel
GET    /api/market/chart/:symbol     # Données graphique
GET    /api/market/morocco/:ticker   # Actions Casablanca
Signals
GET    /api/signals/:symbol          # Signal AI pour un symbole
GET    /api/signals/morocco/:ticker  # Signal pour Bourse Casablanca
Leaderboard
GET    /api/leaderboard/monthly      # Classement du mois
Payment
GET    /api/payment/plans            # Plans d'abonnement
POST   /api/payment/checkout         # Checkout (JWT)
GET    /api/payment/history          # Historique paiements (JWT)

🔒 Sécurité
✅ Mots de passe hashés avec bcrypt
✅ Authentification JWT avec expiration
✅ CORS configuré pour origines autorisées uniquement
✅ Validation des inputs côté backend
✅ Variables sensibles dans fichiers .env (non versionnés)

⚠️ Limitations connues
API Yahoo Finance
L'application utilise l'API Yahoo Finance gratuite pour les données de marché des actions internationales. Cette API impose des limitations strictes:

Limitations:

Rate limiting: Nombre maximum de requêtes par heure/IP
Blocages temporaires (Error 429) en cas de dépassement du quota
Indisponibilité intermittente pour les actions internationales en production

État actuel:

✅ Fonctionnel à 100%: 
Actions de la Bourse de Casablanca (IAM, ATTIJARIWAFA, BCP, BMCE, etc.)
Authentification (inscription/connexion)
Actions de la Bourse de Casablanca (IAM, ATTIJARIWAFA, BCP, BMCE, etc.)
Prix en temps réel pour actions marocaines
Signaux de trading IA pour actions marocaines
Interface utilisateur complète
Trading virtuel

⚠️ Limité temporairement: Actions internationales (AAPL, GOOGL, MSFT, etc.)
Fonctionnent parfaitement en environnement local
Peuvent être bloquées temporairement en production (rate limiting Yahoo Finance)
Leaderboard (nécessite données de test ou utilisateurs réels)
Statistiques de challenge (nécessite activité de trading)

✅ Fonctionnel à 100% en local: Toutes les fonctionnalités marchent parfaitement en environnement de développement local

Solutions implémentées:

Système de fallback avec données de démonstration
Messages d'erreur clairs pour l'utilisateur
Focus sur les actions marocaines qui fonctionnent parfaitement

Améliorations futures:

Migration vers API payante (Alpha Vantage Pro, Finnhub, IEX Cloud)
Système de cache Redis pour réduire les appels API
Base de données de prix historiques

Note sur le déploiement
L'application a été déployée sur PythonAnywhere (backend) et Vercel (frontend) au lieu de Render/Railway, car ces derniers nécessitent une carte bancaire pour leurs plans gratuits, ce qui n'était pas accessible pour ce projet académique.

🐛 Problèmes connus et solutions
CORS Errors
Si vous rencontrez des erreurs CORS, vérifiez que votre URL frontend est ajoutée dans app.py:

python
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:5173",
    "https://votre-domaine-vercel.app"
]}})
Database Errors sur PythonAnywhere
Utilisez /tmp/tradesense.db au lieu d'un chemin absolu pour éviter les problèmes de permissions.

Actions internationales indisponibles
Si les actions internationales ne s'affichent pas:

Attendez 1-2 heures (levée automatique du rate limiting)
Utilisez les actions marocaines qui fonctionnent parfaitement
Testez en environnement local où les limitations sont moins strictes

📝 Améliorations futures
 Migration vers PostgreSQL pour production
 Implémentation de WebSockets pour prix temps réel
 Ajout de tests unitaires et d'intégration
 Intégration de vraies APIs de marché (Alpha Vantage, Yahoo Finance)
 Système de notifications push
 Support multi-devises (USD, EUR, MAD)
 Application mobile (React Native)


👨‍💻 Auteur
Fatima Zahra Réghini Idrissi

GitHub: @fatidrissi0
Projet: TradeSense AI

📄 Licence
Ce projet a été développé dans un cadre académique.

🙏 Remerciements
Merci au professeur pour les enseignements et le support
Communauté open-source pour les packages utilisés
PythonAnywhere et Vercel pour les services de déploiement gratuits

📞 Support
Pour toute question ou problème:

Ouvrir une Issue
Consulter la documentation ci-dessus
Vérifier les logs d'erreur dans la console du navigateur (F12)
Fait avec ❤️ pour le projet de fin de module

