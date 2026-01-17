from flask import Blueprint, request, jsonify
from datetime import datetime
from services.market_data import get_live_price, get_chart_data, SUPPORTED_SYMBOLS
from services.morocco_scraper import scrape_casablanca_stock, get_supported_morocco_tickers

market_bp = Blueprint('market', __name__)

@market_bp.route('/api/market/live/<symbol>', methods=['GET'])
def get_live_market_data(symbol):
    """
    Récupère les données de marché en direct pour un symbole
    
    Args:
        symbol (str): Le symbole boursier (ex: 'AAPL', 'BTC-USD')
    
    Returns:
        JSON: Données de prix en direct
    """
    try:
        # Appeler la fonction du service
        result = get_live_price(symbol.upper())
        
        # Vérifier s'il y a une erreur
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur lors de la récupération des données de marché: {str(e)}',
            'symbol': symbol
        }), 500

@market_bp.route('/api/market/chart/<symbol>', methods=['GET'])
def get_chart_market_data(symbol):
    """
    Récupère les données historiques pour un symbole
    
    Args:
        symbol (str): Le symbole boursier
    
    Query Parameters:
        interval (str): L'intervalle de temps (défaut: '1d')
        period (str): La période de temps (défaut: '1mo')
    
    Returns:
        JSON: Données historiques formatées
    """
    try:
        # Récupérer les paramètres de la requête
        interval = request.args.get('interval', '1d')
        period = request.args.get('period', '1mo')
        
        # Appeler la fonction du service
        result = get_chart_data(symbol.upper(), interval, period)
        
        # Vérifier s'il y a une erreur
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), 400
        
        return jsonify({
            'symbol': symbol.upper(),
            'interval': interval,
            'period': period,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur lors de la récupération des données historiques: {str(e)}',
            'symbol': symbol
        }), 500

@market_bp.route('/api/market/symbols', methods=['GET'])
def get_supported_symbols():
    """
    Retourne la liste des symboles supportés
    
    Returns:
        JSON: Liste des symboles supportés
    """
    return jsonify({
        'symbols': SUPPORTED_SYMBOLS,
        'count': len(SUPPORTED_SYMBOLS)
    }), 200

@market_bp.route('/api/market/morocco/<ticker>', methods=['GET'])
def get_morocco_stock_data(ticker):
    """
    Récupère les données d'un titre de la Bourse de Casablanca
    
    Args:
        ticker (str): Le ticker boursier marocain (ex: 'IAM', 'ATW', 'BCP')
    
    Returns:
        JSON: Données boursières du titre marocain
    """
    try:
        # Appeler la fonction du service
        result = scrape_casablanca_stock(ticker.upper())
        
        # Vérifier s'il y a une erreur
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur lors de la récupération des données marocaines: {str(e)}',
            'ticker': ticker
        }), 500

@market_bp.route('/api/market/morocco/symbols', methods=['GET'])
def get_supported_morocco_symbols():
    """
    Retourne la liste des tickers marocains supportés
    
    Returns:
        JSON: Liste des tickers marocains supportés
    """
    try:
        symbols = get_supported_morocco_tickers()
        return jsonify({
            'symbols': symbols,
            'count': len(symbols),
            'source': 'Casablanca Stock Exchange'
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Erreur lors de la récupération des symboles marocains: {str(e)}'
        }), 500