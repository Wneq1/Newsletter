"""
SYSTEM NEWSLETTERA - Wersja Skonsolidowana (PythonAnywhere)
Data konsolidacji: 2026-01-16
"""

# Importy bibliotek standardowych
import os
import sys
import smtplib
import ssl
import re
import traceback
from datetime import datetime
from typing import List, Dict, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Importy bibliotek zewnętrznych
import requests
import feedparser
import yfinance as yf
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# KONFIGURACJA (Config)
# -----------------------------------------------------------------------------

# Ładowanie zmiennych środowiskowych z pliku .env (jeśli istnieje)
load_dotenv()

class Config:
    """Klasa konfiguracyjna dla systemu newslettera."""
    
    # Konfiguracja Email
    _server_str = os.getenv('SMTP_SERVER')
    SMTP_SERVER: str = _server_str if _server_str else 'poczta.o2.pl'
    
    _port_str = os.getenv('SMTP_PORT')
    SMTP_PORT: int = int(_port_str) if _port_str else 465
    
    EMAIL_SENDER: str = os.getenv('EMAIL_SENDER', '')
    EMAIL_PASSWORD: str = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_RECIPIENT: str = os.getenv('EMAIL_RECIPIENT', '')
    
    # Strefa czasowa
    TIMEZONE: str = os.getenv('TZ', 'Europe/Warsaw')
    
    @classmethod
    def validate(cls) -> bool:
        """Waliduje czy cała wymagana konfiguracja jest obecna."""
        required_fields = [
            ('EMAIL_SENDER', cls.EMAIL_SENDER),
            ('EMAIL_PASSWORD', cls.EMAIL_PASSWORD),
            ('EMAIL_RECIPIENT', cls.EMAIL_RECIPIENT),
        ]
        
        missing_fields = []
        for field_name, field_value in required_fields:
            if not field_value:
                missing_fields.append(field_name)
        
        if missing_fields:
            print(f"[BŁĄD] Brakująca konfiguracja: {', '.join(missing_fields)}")
            print("Upewnij się, że zmienne środowiskowe są ustawione (np. w pliku .env)")
            return False
            
        return True
    
    @classmethod
    def display_config(cls) -> None:
        """Wyświetla obecną konfigurację (ukrywając wrażliwe dane)."""
        print("[EMAIL] Konfiguracja Newslettera:")
        print(f"  Serwer SMTP: {cls.SMTP_SERVER}:{cls.SMTP_PORT}")
        print(f"  Nadawca: {cls.EMAIL_SENDER}")
        print(f"  Odbiorca: {cls.EMAIL_RECIPIENT}")
        print(f"  Hasło: {'*' * len(cls.EMAIL_PASSWORD) if cls.EMAIL_PASSWORD else 'NIE USTAWIONO'}")
        print(f"  Strefa czasowa: {cls.TIMEZONE}")


# -----------------------------------------------------------------------------
# NARZĘDZIA (Utils)
# -----------------------------------------------------------------------------

def strip_html_tags(text: str) -> str:
    """Usuwa znaczniki HTML i czyści treść tekstową."""
    if not text:
        return ""
    
    # Usuwanie znaczników HTML
    text = re.sub(r'<[^>]+>', '', text)
    # Usuwanie nadmiarowych białych znaków
    text = re.sub(r'\s+', ' ', text)
    
    # Dekodowanie encji HTML
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('<![CDATA[', '')
    text = text.replace(']]>', '')
    
    return text.strip()


# -----------------------------------------------------------------------------
# WYSYŁANIE EMAILI (Email Sender)
# -----------------------------------------------------------------------------

def send_email(subject: str, html_content: str, recipient: Optional[str] = None) -> bool:
    """Wysyła email HTML przez SMTP."""
    config = Config()
    
    if not config.validate():
        print("[BŁĄD] Nieprawidłowa konfiguracja email")
        return False
    
    to_email = recipient or config.EMAIL_RECIPIENT
    
    try:
        # Tworzenie wiadomości
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = config.EMAIL_SENDER
        message['To'] = to_email
        
        # Dołączanie treści HTML
        html_part = MIMEText(html_content, 'html', 'utf-8')
        message.attach(html_part)
        
        print(f"[EMAIL] Łączenie z {config.SMTP_SERVER}:{config.SMTP_PORT}...")
        
        context = ssl.create_default_context()
        
        if config.SMTP_PORT == 465:
            # Połączenie SSL (np. poczta.o2.pl, gmail na 465)
            with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, context=context) as server:
                print(f"Logowanie jako {config.EMAIL_SENDER}...")
                server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
                print(f"Wysyłanie emaila do {to_email}...")
                server.send_message(message)
        else:
            # Połączenie STARTTLS (np. gmail na 587)
            with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.starttls(context=context)
                print(f"Logowanie jako {config.EMAIL_SENDER}...")
                server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
                print(f"Wysyłanie emaila do {to_email}...")
                server.send_message(message)
            
        print("[OK] Email wysłany pomyślnie!")
        return True
        
    except Exception as e:
        print(f"[BŁĄD] Błąd podczas wysyłania emaila: {e}")
        return False


# -----------------------------------------------------------------------------
# GENEROWANIE HTML (HTML Template)
# -----------------------------------------------------------------------------

def get_css_styles() -> str:
    """Pobiera style CSS dla szablonu emaila."""
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; padding: 20px; line-height: 1.6; }
        .container { max-width: 800px; margin: 0 auto; background-color: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .date { font-size: 16px; opacity: 0.9; }
        .section { padding: 30px; border-bottom: 1px solid #e0e0e0; }
        .section:last-of-type { border-bottom: none; }
        .section-title { font-size: 24px; margin-bottom: 20px; color: #333; border-left: 4px solid #667eea; padding-left: 15px; }
        .world .section-title { border-left-color: #3498db; }
        .poland .section-title { border-left-color: #e74c3c; }
        .finance .section-title { border-left-color: #f39c12; }
        .news-item { margin-bottom: 25px; padding: 15px; background-color: #f9f9f9; border-radius: 8px; transition: transform 0.2s; }
        .news-item:hover { transform: translateX(5px); background-color: #f0f0f0; }
        .news-item h3 { font-size: 18px; margin-bottom: 8px; color: #2c3e50; }
        .news-item h3 a { color: #2c3e50; text-decoration: none; }
        .news-item h3 a:hover { color: #667eea; }
        .news-meta { font-size: 12px; color: #7f8c8d; margin-bottom: 8px; }
        .news-summary { font-size: 14px; color: #555; line-height: 1.5; }
        .financial-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .metal-card { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 10px; text-align: center; }
        .metal-name { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #2c3e50; }
        .metal-price { font-size: 32px; font-weight: bold; color: #27ae60; margin: 10px 0; }
        .metal-change { font-size: 14px; margin: 5px 0; }
        .positive { color: #27ae60; }
        .negative { color: #e74c3c; }
        .footer { background-color: #34495e; color: white; padding: 20px; text-align: center; }
        .footer .small { font-size: 12px; opacity: 0.8; margin-top: 5px; }
        .read-more { display: inline-block; margin-top: 8px; color: #667eea; text-decoration: none; font-size: 13px; font-weight: bold; }
        .read-more:hover { text-decoration: underline; }
    """

def create_news_section(title: str, news_items: List[Dict], section_class: str) -> str:
    """Tworzy sekcję wiadomości."""
    if not news_items:
        return f"""<div class="section {section_class}"><h2 class="section-title">{title}</h2><p>Brak dostępnych wiadomości.</p></div>"""
    
    items_html = ""
    for item in news_items:
        items_html += f"""
        <div class="news-item">
            <h3><a href="{item.get('link', '#')}" target="_blank">{item.get('title', 'Brak tytułu')}</a></h3>
            <div class="news-meta">[NEWS] {item.get('source', 'Nieznane źródło')} • {item.get('published', 'Nieznana data')}</div>
            <div class="news-summary">{item.get('summary', 'Brak opisu')[:200]}...</div>
            <a href="{item.get('link', '#')}" class="read-more" target="_blank">Czytaj więcej →</a>
        </div>
        """
    return f"""<div class="section {section_class}"><h2 class="section-title">{title}</h2>{items_html}</div>"""

def create_financial_section(gold, silver) -> str:
    """Tworzy sekcję danych finansowych."""
    
    def create_card(data, label, default_icon):
        if 'error' in data:
            return f"""<div class="metal-card"><div class="metal-name">⚠️ [{label}] {data.get('name', label)}</div>
                       <div class="news-summary" style="text-align: center; padding: 20px;">{data.get('error', 'Niedostępne')}</div></div>"""
        
        change_class = 'positive' if data.get('daily_change', 0) >= 0 else 'negative'
        arrow = '↑' if data.get('daily_change', 0) >= 0 else '↓'
        currency = data.get('currency', 'USD')
        symbol = '$' if currency == 'USD' else f' {currency}'
        price = f"{symbol}{data.get('price', 'N/A')}" if currency == 'USD' else f"{data.get('price', 'N/A')}{symbol}"
        unit = f" / {data.get('unit', '')}" if data.get('unit') else ""
        
        return f"""
        <div class="metal-card">
            <div class="metal-name">[{label}] {data.get('name', label)}</div>
            <div class="metal-price">{price}<span style="font-size: 16px; color: #7f8c8d;">{unit}</span></div>
            <div class="metal-change {change_class}">{arrow} Dziś: {data.get('daily_change', 0):+.2f} ({data.get('daily_change_percent', 0):+.2f}%)</div>
            <div class="metal-change {change_class}">Miesiąc: {data.get('weekly_change', 0):+.2f} ({data.get('weekly_change_percent', 0):+.2f}%)</div>
        </div>
        """
            
    gold_html = create_card(gold, "ZŁOTO", "🟡")
    silver_html = create_card(silver, "SREBRO", "⚪")
    
    return f"""
    <div class="section finance">
        <h2 class="section-title">📊 Rynki Finansowe</h2>
        <div class="financial-grid">{gold_html}{silver_html}</div>
    </div>
    """

def generate_newsletter_html(world_news, polish_news, bankier_news, financial_data) -> str:
    """Generuje kompletny newsletter HTML."""
    date_str = datetime.now().strftime("%d.%m.%Y")
    return f"""
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Codzienny Newsletter - {date_str}</title>
        <style>{get_css_styles()}</style>
    </head>
    <body>
        <div class="container">
            <div class="header"><h1>[NEWS] Codzienny Newsletter</h1><p class="date">{date_str}</p></div>
            {create_news_section("[ŚWIAT] Wiadomości ze Świata", world_news, "world")}
            {create_news_section("[POLSKA] Wiadomości z Polski", polish_news, "poland")}
            {create_news_section("💰 [FINANSE] Bankier.pl", bankier_news, "finance")}
            {create_financial_section(financial_data.get('gold', {}), financial_data.get('silver', {}))}
            <div class="footer"><p>Newsletter wygenerowany automatycznie</p><p class="small">{datetime.now().strftime("%d.%m.%Y %H:%M")}</p></div>
        </div>
    </body>
    </html>
    """

# -----------------------------------------------------------------------------
# SCRAPER: ŚWIAT (World News - BBC)
# -----------------------------------------------------------------------------

def fetch_world_news() -> List[Dict[str, str]]:
    """Pobiera wiadomości z BBC (Top Stories & World)."""
    news_sources = [
        {'url': 'http://feeds.bbci.co.uk/news/rss.xml', 'name': 'BBC Info'},
        {'url': 'http://feeds.bbci.co.uk/news/world/rss.xml', 'name': 'BBC World'}
    ]
    all_news = []
    seen_links = set()
    
    for source in news_sources:
        try:
            feed = feedparser.parse(source['url'])
            for entry in feed.entries[:5]:
                link = entry.get('link', '')
                if link in seen_links: continue
                seen_links.add(link)
                
                all_news.append({
                    'title': entry.get('title', 'Brak tytułu'),
                    'summary': entry.get('summary', entry.get('description', 'Brak opisu')),
                    'link': link,
                    'source': source['name'],
                    'published': entry.get('published', 'Nieznana data')
                })
        except Exception as e:
            print(f"[OSTRZEŻENIE] Błąd pobierania z {source['name']}: {e}")
            continue
    return all_news[:3]

# -----------------------------------------------------------------------------
# SCRAPER: POLSKA (Polish News - Gazeta Wyborcza)
# -----------------------------------------------------------------------------

def fetch_polish_news() -> List[Dict[str, str]]:
    """Pobiera wiadomości z Gazety Wyborczej (Kraj)."""
    source = {'url': 'http://rss.gazeta.pl/pub/rss/gazetawyborcza_kraj.xml', 'name': 'Gazeta Wyborcza - Kraj'}
    all_news = []
    
    try:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:5]:
            raw_summary = entry.get('summary', entry.get('description', 'Brak opisu'))
            clean_summary = strip_html_tags(raw_summary)
            if len(clean_summary) > 200: clean_summary = clean_summary[:200] + '...'
            
            all_news.append({
                'title': strip_html_tags(entry.get('title', 'Brak tytułu')),
                'summary': clean_summary,
                'link': entry.get('link', ''),
                'source': source['name'],
                'published': entry.get('published', 'Nieznana data')
            })
    except Exception as e:
        print(f"[OSTRZEŻENIE] Błąd pobierania z {source['name']}: {e}")
            
    return all_news[:3]

# -----------------------------------------------------------------------------
# SCRAPER: BANKIER (Financial News - Bankier.pl)
# -----------------------------------------------------------------------------

def fetch_bankier_news() -> List[Dict[str, str]]:
    """Pobiera wiadomości z Bankier.pl."""
    source = {'url': 'https://www.bankier.pl/rss/wiadomosci.xml', 'name': 'Bankier.pl'}
    all_news = []
    
    try:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:5]:
            raw_summary = entry.get('summary', entry.get('description', 'Brak opisu'))
            clean_summary = strip_html_tags(raw_summary)
            if len(clean_summary) > 200: clean_summary = clean_summary[:200] + '...'
            
            all_news.append({
                'title': strip_html_tags(entry.get('title', 'Brak tytułu')),
                'summary': clean_summary,
                'link': entry.get('link', ''),
                'source': source['name'],
                'published': entry.get('published', 'Nieznana data')
            })
    except Exception as e:
        print(f"[OSTRZEŻENIE] Błąd pobierania z {source['name']}: {e}")
            
    return all_news[:3]

# -----------------------------------------------------------------------------
# SCRAPER: DANE FINANSOWE (Metale, Waluty)
# -----------------------------------------------------------------------------

def fetch_stooq_history(symbol: str) -> Dict[str, any]:
    """Pobiera dane historyczne ze Stooq."""
    try:
        url = f"https://stooq.pl/q/d/l/?s={symbol}&i=d"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text.strip().split('\n')
            lines = [line.split(',') for line in content[1:] if line]
            
            if len(lines) >= 1:
                current = lines[-1]
                price = float(current[4])
                
                daily_change = 0.0
                daily_change_percent = 0.0
                monthly_change = 0.0
                monthly_change_percent = 0.0
                
                if len(lines) >= 2:
                    prev = lines[-2]
                    try:
                        prev_close = float(prev[4])
                        daily_change = price - prev_close
                        daily_change_percent = (daily_change / prev_close) * 100
                    except (ValueError, IndexError): pass
                    
                if len(lines) >= 22:
                    month_ago = lines[-22]
                    try:
                        month_close = float(month_ago[4])
                        monthly_change = price - month_close
                        monthly_change_percent = (monthly_change / month_close) * 100
                    except (ValueError, IndexError): pass
                elif len(lines) >= 2:
                    month_ago = lines[0]
                    try:
                        month_close = float(month_ago[4])
                        monthly_change = price - month_close
                        monthly_change_percent = (monthly_change / month_close) * 100
                    except: pass
                     
                return {
                    'price': price, 'daily_change': daily_change, 'daily_change_percent': daily_change_percent,
                    'monthly_change': monthly_change, 'monthly_change_percent': monthly_change_percent
                }
    except Exception as e:
        print(f"[OSTRZEŻENIE] Błąd w fetch_stooq_history dla {symbol}: {e}")
    return None

def get_fallback_data(name: str) -> Dict:
    return {'symbol': '---', 'name': name, 'price': 0.0, 'currency': '-', 
            'daily_change': 0.0, 'daily_change_percent': 0.0, 'weekly_change': 0.0, 'weekly_change_percent': 0.0,
            'error': 'Dane tymczasowo niedostępne'}

def get_gold_price() -> Dict:
    stooq_data = fetch_stooq_history('xaupln')
    if stooq_data:
        return {
            'symbol': 'XAU/PLN', 'name': 'Złoto', 'price': round(stooq_data['price'], 2), 'currency': 'PLN', 'unit': 'uncja',
            'daily_change': round(stooq_data['daily_change'], 2), 'daily_change_percent': round(stooq_data['daily_change_percent'], 2),
            'weekly_change': round(stooq_data['monthly_change'], 2), 'weekly_change_percent': round(stooq_data['monthly_change_percent'], 2)
        }
    return get_fallback_data('Złoto')

def get_silver_price() -> Dict:
    stooq_data = fetch_stooq_history('xagpln')
    if stooq_data:
        return {
            'symbol': 'XAG/PLN', 'name': 'Srebro', 'price': round(stooq_data['price'], 2), 'currency': 'PLN', 'unit': 'uncja',
            'daily_change': round(stooq_data['daily_change'], 2), 'daily_change_percent': round(stooq_data['daily_change_percent'], 2),
            'weekly_change': round(stooq_data['monthly_change'], 2), 'weekly_change_percent': round(stooq_data['monthly_change_percent'], 2)
        }
    return get_fallback_data('Srebro')

def fetch_financial_data() -> Dict:
    return {'gold': get_gold_price(), 'silver': get_silver_price()}


# -----------------------------------------------------------------------------
# GŁÓWNA LOGIKA (Main)
# -----------------------------------------------------------------------------

def collect_all_news() -> Dict:
    """Pobiera wiadomości ze wszystkich źródeł."""
    news_data = {'world_news': [], 'polish_news': [], 'bankier_news': [], 'financial_data': {}}
    
    print("  [ŚWIAT] Pobieranie wiadomości ze świata...")
    try: news_data['world_news'] = fetch_world_news()
    except Exception as e: print(f"     [BŁĄD] {e}")
    print(f"     [OK] Pobrano {len(news_data['world_news'])}")
    
    print("  [POLSKA] Pobieranie wiadomości z Polski...")
    try: news_data['polish_news'] = fetch_polish_news()
    except Exception as e: print(f"     [BŁĄD] {e}")
    print(f"     [OK] Pobrano {len(news_data['polish_news'])}")
    
    print("  [BANKIER] Pobieranie wiadomości z Bankier.pl...")
    try: news_data['bankier_news'] = fetch_bankier_news()
    except Exception as e: print(f"     [BŁĄD] {e}")
    print(f"     [OK] Pobrano {len(news_data['bankier_news'])}")
    
    print("  [FINANSE] Pobieranie danych finansowych...")
    try: news_data['financial_data'] = fetch_financial_data()
    except Exception as e: print(f"     [BŁĄD] {e}")
    print(f"     [OK] Pobrano dane finansowe")
    
    return news_data

def main() -> int:
    print("=" * 60)
    print("[NEWS] SYSTEM CODZIENNEGO NEWSLETTERA (Wersja Skonsolidowana)")
    print("=" * 60)
    print(f"[CZAS] Rozpoczęto: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        print("[1/4] Walidacja konfiguracji...")
        config = Config()
        if not config.validate(): return 1
        config.display_config()
        
        print("\n[2/4] Pobieranie wiadomości...")
        news_data = collect_all_news()
        
        print("\n[3/4] Generowanie HTML...")
        html_content = generate_newsletter_html(
            news_data['world_news'], news_data['polish_news'],
            news_data['bankier_news'], news_data['financial_data']
        )
        
        print("\n[4/4] Wysyłanie emaila...")
        sender_email = config.EMAIL_SENDER
        recipient_email = config.EMAIL_RECIPIENT
        current_date = datetime.now().strftime("%d.%m.%Y")
        subject = f"[NEWS] Codzienny Newsletter - {current_date}"
        
        if send_email(subject, html_content):
            print("\n" + "=" * 60)
            print("[OK] NEWSLETTER WYSŁANY POMYŚLNIE!")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("[BŁĄD] NIE UDAŁO SIĘ WYSŁAĆ NEWSLETTERA")
            print("=" * 60)
            return 1
            
    except Exception as e:
        print(f"\n[BŁĄD] BŁĄD KRYTYCZNY: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
