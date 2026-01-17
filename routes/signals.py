from flask import Blueprint, jsonify
import yfinance as yf

from services.ai_signals import generate_signal
from services.morocco_scraper import scrape_casablanca_stock


signals_bp = Blueprint("signals", __name__)


@signals_bp.route("/api/signals/<symbol>", methods=["GET"])
def get_signal(symbol):
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="3mo")

        if history is None or history.empty or "Close" not in history.columns:
            return jsonify({"error": "Historique indisponible", "symbol": symbol}), 400

        closes = history["Close"].dropna()
        if closes.empty:
            return jsonify({"error": "Historique indisponible", "symbol": symbol}), 400

        price_history = [{"close": float(v)} for v in closes.tolist()]
        result = generate_signal(symbol.upper(), price_history)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la génération du signal: {str(e)}", "symbol": symbol}), 500

@signals_bp.route("/api/signals/morocco/<ticker>", methods=["GET"])
def get_morocco_signal(ticker):
    """
    Génère un signal simple pour les tickers marocains à partir du pourcentage de variation.
    Heuristique:
      - change_percent > +1.0 -> BUY (confidence min 60, risque low)
      - change_percent < -1.0 -> SELL (confidence min 60, risque low)
      - sinon -> HOLD (confidence 50, risque medium)
    """
    try:
        data = scrape_casablanca_stock(ticker.upper())
        if "error" in data:
            return jsonify({"error": data["error"], "symbol": ticker}), 400

        change = float(data.get("change_percent", 0.0))
        signal = "HOLD"
        confidence = 50
        risk_level = "medium"
        reason = "No strong signal detected"

        abs_change = abs(change)
        if change > 1.0:
            signal = "BUY"
            confidence = int(min(90, 60 + abs_change * 10))
            risk_level = "low"
            reason = f"Positive momentum ({change:.2f}%)"
        elif change < -1.0:
            signal = "SELL"
            confidence = int(min(90, 60 + abs_change * 10))
            risk_level = "low"
            reason = f"Negative momentum ({change:.2f}%)"

        return jsonify({
            "signal": signal,
            "confidence": confidence,
            "risk_level": risk_level,
            "reason": reason,
            "indicators": {
                "change_percent": change,
                "currency": data.get("currency", "MAD"),
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erreur lors du signal Maroc: {str(e)}", "symbol": ticker}), 500
