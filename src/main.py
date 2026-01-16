"""
Główny koordynator Newslettera
Zarządza wszystkimi komponentami w celu pobrania wiadomości i wysłania codziennego newslettera.
"""

import sys
from datetime import datetime
from typing import Dict, List
import traceback

# Import wszystkich modułów
from config import Config
from scrapers.world_news import fetch_world_news
from scrapers.polish_news import fetch_polish_news
from scrapers.bankier_news import fetch_bankier_news
from scrapers.financial_news import fetch_financial_data
from html_template import generate_newsletter_html
from email_sender import send_email


def main() -> int:
    """
    Główny punkt wejścia dla systemu newslettera.
    
    Zwraca:
        Kod wyjścia (0 dla sukcesu, 1 dla błędu)
    """
    print("=" * 60)
    print("[NEWS] SYSTEM CODZIENNEGO NEWSLETTERA")
    print("=" * 60)
    print(f"[CZAS] Rozpoczęto: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Krok 1: Walidacja konfiguracji
        print("[KONFIGURACJA] Krok 1: Walidacja konfiguracji...")
        config = Config()
        if not config.validate():
            print("[BŁĄD] Walidacja konfiguracji nie powiodła się!")
            return 1
        config.display_config()
        print("[OK] Konfiguracja poprawna\n")
        
        # Krok 2: Pobieranie wiadomości
        print("[POBIERANIE] Krok 2: Pobieranie wiadomości ze wszystkich źródeł...")
        news_data = collect_all_news()
        print("[OK] Pobieranie wiadomości zakończone\n")
        
        # Krok 3: Generowanie newslettera HTML
        print("[HTML] Krok 3: Generowanie newslettera HTML...")
        html_content = generate_newsletter(news_data)
        print("[OK] Newsletter HTML wygenerowany\n")
        
        # Krok 4: Wysyłanie emaila
        print("[EMAIL] Krok 4: Wysyłanie emaila z newsletterem...")
        success = send_newsletter(html_content)
        
        if success:
            print("\n" + "=" * 60)
            print("[OK] NEWSLETTER WYSŁANY POMYŚLNIE!")
            print("=" * 60)
            log_execution(success=True)
            return 0
        else:
            print("\n" + "=" * 60)
            print("[BŁĄD] WYSYŁANIE NEWSLETTERA NIE POWIODŁO SIĘ!")
            print("=" * 60)
            log_execution(success=False, error="Wysyłanie emaila nie powiodło się")
            return 1
            
    except Exception as e:
        print(f"\n[BŁĄD] BŁĄD KRYTYCZNY: {e}")
        print("\nŚlad stosu (Stack trace):")
        traceback.print_exc()
        log_execution(success=False, error=str(e))
        return 1


def collect_all_news() -> Dict:
    """
    Pobiera wiadomości ze wszystkich źródeł.
    
    Zwraca:
        Słownik zawierający wszystkie pobrane dane wiadomości
    """
    news_data = {
        'world_news': [],
        'polish_news': [],
        'bankier_news': [],
        'financial_data': {}
    }
    
    # Pobieranie wiadomości ze świata
    try:
        print("  [ŚWIAT] Pobieranie wiadomości ze świata...")
        news_data['world_news'] = fetch_world_news()
        print(f"     [OK] Pobrano {len(news_data['world_news'])} wiadomości ze świata")
    except Exception as e:
        print(f"     [OSTRZEŻENIE] Błąd podczas pobierania wiadomości ze świata: {e}")
    
    # Pobieranie wiadomości z Polski
    try:
        print("  [POLSKA] Pobieranie wiadomości z Polski...")
        news_data['polish_news'] = fetch_polish_news()
        print(f"     [OK] Pobrano {len(news_data['polish_news'])} wiadomości z Polski")
    except Exception as e:
        print(f"     [OSTRZEŻENIE] Błąd podczas pobierania wiadomości z Polski: {e}")
    
    # Pobieranie wiadomości z Bankiera (zamiast Tech)
    try:
        print("  [BANKIER] Pobieranie wiadomości z Bankier.pl...")
        news_data['bankier_news'] = fetch_bankier_news()
        print(f"     [OK] Pobrano {len(news_data['bankier_news'])} wiadomości z Bankiera")
    except Exception as e:
        print(f"     [OSTRZEŻENIE] Błąd podczas pobierania wiadomości z Bankiera: {e}")
    
    # Pobieranie danych finansowych
    try:
        print("  [FINANSE] Pobieranie danych finansowych...")
        news_data['financial_data'] = fetch_financial_data()
        print(f"     [OK] Pobrano dane finansowe (Złoto, Srebro, Trendy)")
    except Exception as e:
        print(f"     [OSTRZEŻENIE] Błąd podczas pobierania danych finansowych: {e}")
    
    return news_data


def generate_newsletter(news_data: Dict) -> str:
    """
    Generuje newsletter HTML z pobranych danych.
    
    Argumenty:
        news_data: Słownik zawierający wszystkie pobrane wiadomości
        
    Zwraca:
        Treść HTML newslettera
    """
    # Generowanie HTML
    html_content = generate_newsletter_html(
        world_news=news_data['world_news'],
        polish_news=news_data['polish_news'],
        bankier_news=news_data['bankier_news'],
        financial_data=news_data['financial_data']
    )
    
    return html_content


def send_newsletter(html_content: str) -> bool:
    """
    Wysyła email z newsletterem.
    
    Argumenty:
        html_content: Treść HTML do wysłania
        
    Zwraca:
        True jeśli wysłano pomyślnie, False w przeciwnym razie
    """
    current_date = datetime.now().strftime("%d.%m.%Y")
    subject = f"[NEWS] Codzienny Newsletter - {current_date}"
    
    return send_email(subject=subject, html_content=html_content)


def log_execution(success: bool, error: str = None) -> None:
    """
    Loguje status wykonania.
    
    Argumenty:
        success: Czy wykonanie się powiodło
        error: Komunikat błędu jeśli wystąpił
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "SUKCES" if success else "PORAŻKA"
    
    log_message = f"[{timestamp}] Wykonanie Newslettera: {status}"
    if error:
        log_message += f" - Błąd: {error}"
    
    print(f"\n[LOG] {log_message}")
    
    # Opcjonalnie zapisz do pliku logów
    try:
        with open('newsletter.log', 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    except Exception as e:
        print(f"[OSTRZEŻENIE] Nie można zapisać do pliku logów: {e}")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
