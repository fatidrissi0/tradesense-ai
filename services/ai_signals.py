import numpy as np


def calculate_rsi(prices, period=14):
    prices_arr = np.asarray(prices, dtype=float)
    if prices_arr.size < 2:
        return 50.0

    deltas = np.diff(prices_arr)
    window = deltas[-period:] if deltas.size >= period else deltas

    gains = np.where(window > 0, window, 0.0)
    losses = np.where(window < 0, -window, 0.0)

    avg_gain = float(np.mean(gains)) if gains.size else 0.0
    avg_loss = float(np.mean(losses)) if losses.size else 0.0

    if avg_gain == 0.0 and avg_loss == 0.0:
        return 50.0
    if avg_loss == 0.0:
        return 100.0
    if avg_gain == 0.0:
        return 0.0

    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return float(np.clip(rsi, 0.0, 100.0))


def calculate_ma(prices, period):
    prices_arr = np.asarray(prices, dtype=float)
    if prices_arr.size == 0:
        return 0.0
    if prices_arr.size < period:
        return float(np.mean(prices_arr))
    return float(np.mean(prices_arr[-period:]))


def generate_signal(symbol, price_history):
    prices = [float(p["close"]) for p in price_history if p.get("close") is not None]
    if len(prices) < 2:
        raise ValueError("price_history insuffisant")

    current_price = float(prices[-1])
    rsi = float(calculate_rsi(prices))
    ma20 = float(calculate_ma(prices, 20))
    ma50 = float(calculate_ma(prices, 50))

    signal = "HOLD"
    confidence = 50
    risk_level = "medium"
    reason = "No strong signal detected"

    if rsi < 30 and current_price > ma20:
        signal = "BUY"
        confidence = int(round(60 + (30 - rsi)))
        risk_level = "low"
        reason = f"RSI oversold ({rsi:.2f}) and price above MA20"
    elif rsi > 70 and current_price < ma20:
        signal = "SELL"
        confidence = int(round(60 + (rsi - 70)))
        risk_level = "low"
        reason = f"RSI overbought ({rsi:.2f}) and price below MA20"
    elif ma20 > ma50 and rsi > 50:
        signal = "BUY"
        confidence = 65
        risk_level = "medium"
        reason = "Bullish crossover detected"
    elif ma20 < ma50 and rsi < 50:
        signal = "SELL"
        confidence = 65
        risk_level = "medium"
        reason = "Bearish crossover detected"

    confidence = int(np.clip(confidence, 0, 100))

    return {
        "signal": signal,
        "confidence": confidence,
        "risk_level": risk_level,
        "reason": reason,
        "indicators": {
            "rsi": rsi,
            "ma20": ma20,
            "ma50": ma50,
            "current_price": current_price,
        },
    }
