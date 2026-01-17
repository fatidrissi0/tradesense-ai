import yfinance as yf
from datetime import datetime

# Symboles supportés
SUPPORTED_SYMBOLS = ['AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT', 'BTC-USD', 'ETH-USD']

def get_live_price(symbol):
    """
    Récupère le prix en direct d'un symbole boursier
    
    Args:
        symbol (str): Le symbole boursier (ex: 'AAPL', 'BTC-USD')
    
    Returns:
        dict: Dictionnaire contenant les informations de prix
    """
    try:
        # Vérifier si le symbole est supporté
        if symbol not in SUPPORTED_SYMBOLS:
            return {
                'error': f'Symbole non supporté. Symboles supportés: {", ".join(SUPPORTED_SYMBOLS)}',
                'symbol': symbol
            }
        
        # Créer le ticker
        ticker = yf.Ticker(symbol)
        
        # Récupérer les informations
        info = ticker.info
        
        # Obtenir le prix actuel et le prix de clôture précédent
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        previous_close = info.get('previousClose')
        
        if current_price is None or previous_close is None:
            return {
                'error': 'Impossible de récupérer les données de prix',
                'symbol': symbol
            }
        
        # Calculer le pourcentage de changement
        change_percent = ((current_price - previous_close) / previous_close) * 100
        
        return {
            'symbol': symbol,
            'price': round(float(current_price), 2),
            'change_percent': round(float(change_percent), 2),
            'timestamp': datetime.utcnow().isoformat(),
            'currency': info.get('currency', 'USD')
        }
        
    except Exception as e:
        return {
            'error': f'Erreur lors de la récupération des données: {str(e)}',
            'symbol': symbol
        }

def get_chart_data(symbol, interval='1d', period='1mo'):
    """
    Récupère les données historiques d'un symbole boursier
    
    Args:
        symbol (str): Le symbole boursier
        interval (str): L'intervalle de temps ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        period (str): La période de temps ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        list: Liste de dictionnaires contenant les données de prix
    """
    try:
        # Vérifier si le symbole est supporté
        if symbol not in SUPPORTED_SYMBOLS:
            return {
                'error': f'Symbole non supporté. Symboles supportés: {", ".join(SUPPORTED_SYMBOLS)}',
                'symbol': symbol
            }
        
        # Créer le ticker
        ticker = yf.Ticker(symbol)
        
        # Récupérer l'historique
        hist = ticker.history(period=period, interval=interval)
        
        if hist.empty:
            return {
                'error': 'Aucune donnée historique disponible',
                'symbol': symbol
            }
        
        # Formater les données
        chart_data = []
        for index, row in hist.iterrows():
            chart_data.append({
                'timestamp': index.isoformat(),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            })
        
        return chart_data
        
    except Exception as e:
        return {
            'error': f'Erreur lors de la récupération des données historiques: {str(e)}',
            'symbol': symbol
        }