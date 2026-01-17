import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Données mockées pour la démo
MOCK_DATA = {
    'IAM': {
        'price': 142.50,
        'change_percent': 1.25,
        'company_name': 'Maroc Telecom'
    },
    'ATW': {
        'price': 385.20,
        'change_percent': -0.85,
        'company_name': 'Attijariwafa Bank'
    },
    'BCP': {
        'price': 210.80,
        'change_percent': 0.45,
        'company_name': 'Banque Centrale Populaire'
    },
    'MNG': {
        'price': 439.77,
        'change_percent': -1.67,
        'company_name': 'Managem'
    },
    'SNEP': {
        'price': 512.30,
        'change_percent': 0.95,
        'company_name': 'SNEP'
    }
}

# Cache global pour stocker les résultats
CACHE = {}
CACHE_DURATION = 60  # 60 secondes

def scrape_casablanca_stock(ticker):
    """
    Scrape les données de la Bourse de Casablanca pour un ticker spécifique
    
    Args:
        ticker (str): Le ticker boursier (ex: 'IAM', 'ATW', 'BCP')
    
    Returns:
        dict: Dictionnaire contenant les informations boursières
    """
    ticker = ticker.upper()
    current_time = time.time()
    
    # Vérifier le cache d'abord
    if ticker in CACHE:
        cached_data, timestamp = CACHE[ticker]
        if current_time - timestamp < CACHE_DURATION:
            return cached_data
    
    try:
        # Option 1: Données mockées (pour démo)
        if ticker in MOCK_DATA:
            result = {
                'symbol': ticker,
                'price': MOCK_DATA[ticker]['price'],
                'change_percent': MOCK_DATA[ticker]['change_percent'],
                'timestamp': datetime.utcnow().isoformat(),
                'currency': 'MAD',
                'source': 'Casablanca Stock Exchange (Mock)',
                'company_name': MOCK_DATA[ticker]['company_name']
            }
            
            # Mettre en cache
            CACHE[ticker] = (result, current_time)
            return result
        
        # Option 2: Scraper réel (framework prêt)
        # URL de base pour la Bourse de Casablanca
        base_url = "https://www.boursenews.ma/cotation"
        url = f"{base_url}/{ticker}"
        
        # Faire la requête HTTP
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        
        # Parser le HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Ici, vous devrez adapter le parsing selon la structure HTML réelle du site
        # Exemple générique (à adapter):
        price_element = soup.find('span', class_='price')
        change_element = soup.find('span', class_='change-percent')
        company_element = soup.find('h1', class_='company-name')
        
        if not price_element or not change_element:
            return {
                'error': 'Impossible de parser les données du site',
                'ticker': ticker,
                'url': url
            }
        
        # Extraire les données
        price = float(price_element.text.strip().replace(',', ''))
        change_text = change_element.text.strip()
        change_percent = float(change_text.replace('%', '').replace('+', ''))
        company_name = company_element.text.strip() if company_element else ticker
        
        result = {
            'symbol': ticker,
            'price': price,
            'change_percent': change_percent,
            'timestamp': datetime.utcnow().isoformat(),
            'currency': 'MAD',
            'source': 'Casablanca Stock Exchange',
            'company_name': company_name
        }
        
        # Mettre en cache
        CACHE[ticker] = (result, current_time)
        return result
        
    except requests.exceptions.Timeout:
        return {
            'error': 'Timeout lors de la récupération des données',
            'ticker': ticker
        }
    except requests.exceptions.RequestException as e:
        return {
            'error': f'Erreur de requête HTTP: {str(e)}',
            'ticker': ticker
        }
    except ValueError as e:
        return {
            'error': f'Erreur de parsing des données: {str(e)}',
            'ticker': ticker
        }
    except Exception as e:
        return {
            'error': f'Erreur inattendue: {str(e)}',
            'ticker': ticker
        }

def get_supported_morocco_tickers():
    """
    Retourne la liste des tickers marocains supportés
    
    Returns:
        list: Liste des tickers supportés
    """
    return list(MOCK_DATA.keys())

def clear_cache():
    """
    Vide le cache global
    """
    global CACHE
    CACHE = {}
