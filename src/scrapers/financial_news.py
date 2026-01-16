"""
Skraper Danych Finansowych
Pobiera ceny metali szlachetnych (złoto, srebro) i trendy rynkowe.
"""

import requests
import yfinance as yf
from typing import Dict, List, Optional


def fetch_financial_data() -> Dict[str, any]:
    """
    Pobiera dane finansowe o metalach szlachetnych i trendach rynkowych.
    
    Zwraca:
        Słownik zawierający:
        - gold: Dane o cenie złota (z NBP lub Stooq)
        - silver: Dane o cenie srebra (ze Stooq lub yfinance)
    """
    financial_data = {
        'gold': get_gold_price(),
        'silver': get_silver_price(),
        # 'trends': [] # Trendy tymczasowo usunięte
    }
    
    return financial_data


def fetch_stooq_history(symbol: str) -> Dict[str, any]:
    """
    Pomocnicza funkcja do pobierania i parsowania danych historycznych ze Stooq (CSV).
    Zwraca słownik z ceną, zmianą dzienną i miesięczną lub None.
    """
    try:
        url = f"https://stooq.pl/q/d/l/?s={symbol}&i=d"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text.strip().split('\n')
            # Nagłówek CSV: Date, Open, High, Low, Close, Volume
            # Potrzebujemy co najmniej 2 linii (nagłówek + 1 dana), aby mieć jakąkolwiek cenę
            # Aby obliczyć zmianę dzienną, potrzebujemy 3 linii (Nagłówek + poprzednia + obecna)
            
            lines = [line.split(',') for line in content[1:] if line] # Pomiń nagłówek
            
            if len(lines) >= 1:
                # Ostatni wiersz to bieżące dane
                current = lines[-1]
                # Close (zamknięcie) jest na indeksie 4
                price = float(current[4])
                
                daily_change = 0.0
                daily_change_percent = 0.0
                monthly_change = 0.0
                monthly_change_percent = 0.0
                
                # Zmiana dzienna (vs Poprzednie zamknięcie)
                if len(lines) >= 2:
                    prev = lines[-2]
                    prev_close = float(prev[4])
                    daily_change = price - prev_close
                    daily_change_percent = (daily_change / prev_close) * 100
                    
                # Zmiana miesięczna (vs ~22 dni handlowe temu)
                if len(lines) >= 22:
                    month_ago = lines[-22]
                    month_close = float(month_ago[4])
                    monthly_change = price - month_close
                    monthly_change_percent = (monthly_change / month_close) * 100
                elif len(lines) >= 2: # Fallback jeśli historia jest krótka
                     month_ago = lines[0]
                     month_close = float(month_ago[4])
                     monthly_change = price - month_close
                     monthly_change_percent = (monthly_change / month_close) * 100
                     
                return {
                    'price': price,
                    'daily_change': daily_change,
                    'daily_change_percent': daily_change_percent,
                    'monthly_change': monthly_change,
                    'monthly_change_percent': monthly_change_percent
                }
    except Exception as e:
        print(f"[OSTRZEŻENIE] Błąd w fetch_stooq_history dla {symbol}: {e}")
    
    return None

def get_gold_price() -> Dict[str, any]:
    """
    Pobiera aktualną cenę złota ze Stooq (XAUPLN) z konktekstem historycznym.
    """
    stooq_data = fetch_stooq_history('xaupln')
    
    if stooq_data:
        return {
            'symbol': 'XAU/PLN',
            'name': 'Złoto',
            'price': round(stooq_data['price'], 2),
            'currency': 'PLN',
            'unit': 'uncja',
            'daily_change': round(stooq_data['daily_change'], 2),
            'daily_change_percent': round(stooq_data['daily_change_percent'], 2),
            'weekly_change': round(stooq_data['monthly_change'], 2), # Używamy klucza weekly_change dla mapowania danych miesięcznych w szablonie
            'weekly_change_percent': round(stooq_data['monthly_change_percent'], 2),
            'trend': 'up' if stooq_data['daily_change'] > 0 else 'down'
        }

    # Fallback do NBP jeśli Stooq zawiedzie
    try:
        url_current = "http://api.nbp.pl/api/cenyzlota/last/2/?format=json"
        response = requests.get(url_current, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) >= 2:
                current = data[1]
                prev = data[0]
                price_g = current['cena']
                prev_price_g = prev['cena']
                
                OZ_FACTOR = 31.1034768
                price_oz = price_g * OZ_FACTOR
                prev_price_oz = prev_price_g * OZ_FACTOR
                
                change = price_oz - prev_price_oz
                change_percent = (change / prev_price_oz) * 100
                
                return {
                    'symbol': 'XAU/PLN',
                    'name': 'Złoto (NBP)',
                    'price': round(price_oz, 2),
                    'currency': 'PLN',
                    'unit': 'uncja',
                    'daily_change': round(change, 2),
                    'daily_change_percent': round(change_percent, 2),
                    'weekly_change': 0.0,
                    'weekly_change_percent': 0.0,
                    'trend': 'up' if change > 0 else 'down'
                }
    except Exception as e:
        print(f"[OSTRZEŻENIE] Błąd pobierania złota z NBP: {e}")
        pass
        
    return get_fallback_data('Złoto')


def get_usd_pln_rate() -> float:
    """
    Pobiera aktualny kurs USD/PLN z API NBP.
    """
    try:
        url = "http://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['rates'][0]['mid']
        return 4.0  # Wartość domyślna
    except Exception as e:
        print(f"[OSTRZEŻENIE] Błąd pobierania kursu USD/PLN: {e}")
        return 4.0


def get_silver_price() -> Dict[str, any]:
    """
    Pobiera aktualną cenę srebra ze Stooq (XAGPLN) z kontekstem historycznym.
    """
    stooq_data = fetch_stooq_history('xagpln')
    
    if stooq_data:
        return {
            'symbol': 'XAG/PLN',
            'name': 'Srebro',
            'price': round(stooq_data['price'], 2),
            'currency': 'PLN',
            'unit': 'uncja',
            'daily_change': round(stooq_data['daily_change'], 2),
            'daily_change_percent': round(stooq_data['daily_change_percent'], 2),
            'weekly_change': round(stooq_data['monthly_change'], 2), # Zastąpienie weekly danymi miesięcznymi
            'weekly_change_percent': round(stooq_data['monthly_change_percent'], 2),
            'trend': 'up' if stooq_data['daily_change'] > 0 else 'down'
        }

    # Fallback do yfinance (XAGUSD=X)
    nbp_rate = get_usd_pln_rate()
    try:
        silver = yf.Ticker("XAGUSD=X")
        hist = silver.history(period="1mo") # Pobierz historię z miesiąca
        
        if not hist.empty and len(hist) >= 1:
            usd_price = hist['Close'].iloc[-1]
            price_pln = usd_price * nbp_rate
            
            daily_change = 0.0
            daily_change_percent = 0.0
            monthly_change = 0.0
            monthly_change_percent = 0.0

            if len(hist) >= 2:
                prev_day = hist['Close'].iloc[-2]
                daily_change = (usd_price - prev_day) * nbp_rate
                daily_change_percent = ((usd_price - prev_day) / prev_day) * 100
            
            if len(hist) >= 20:
                month_ago = hist['Close'].iloc[0] # lub -22
                monthly_change = (usd_price - month_ago) * nbp_rate
                monthly_change_percent = ((usd_price - month_ago) / month_ago) * 100
                
            return {
                'symbol': 'Srebro',
                'name': 'Srebro',
                'price': round(price_pln, 2),
                'currency': 'PLN',
                'unit': 'uncja',
                'daily_change': round(daily_change, 2),
                'daily_change_percent': round(daily_change_percent, 2),
                'weekly_change': round(monthly_change, 2),
                'weekly_change_percent': round(monthly_change_percent, 2),
                'trend': 'up' if daily_change > 0 else 'down'
            }
    except Exception as e:
        print(f"[OSTRZEŻENIE] Błąd pobierania srebra z yfinance: {e}")
        pass

    return get_fallback_data('Srebro')


def get_fallback_data(name: str) -> Dict:
    """Dane zapasowe w przypadku awarii API."""
    return {
        'symbol': '---',
        'name': name,
        'price': 0.0,
        'currency': '-',
        'daily_change': 0.0,
        'daily_change_percent': 0.0,
        'weekly_change': 0.0,
        'weekly_change_percent': 0.0,
        'trend': 'unknown',
        'error': 'Dane tymczasowo niedostępne'
    }


if __name__ == "__main__":
    data = fetch_financial_data()
    print("Pobrane dane finansowe:")
    for key, item in data.items():
        if 'error' in item:
             print(f"{key.upper()}: [Błąd] {item['error']}")
        else:
             print(f"{key.upper()}: {item['name']} - {item['price']} {item['currency']} (Zmiana: {item['daily_change_percent']}%)")
