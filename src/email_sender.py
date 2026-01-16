"""
Moduł wysyłania emaili
Obsługuje tworzenie i wysyłanie emaili przez SMTP.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import ssl
from config import Config


def send_email(subject: str, html_content: str, recipient: Optional[str] = None) -> bool:
    """
    Wysyła email HTML przez SMTP.
    
    Argumenty:
        subject: Temat emaila
        html_content: Treść HTML emaila
        recipient: Email odbiorcy (używa domyślnego z konfiguracji jeśli nie podano)
        
    Zwraca:
        True jeśli email został wysłany pomyślnie, False w przeciwnym razie
    """
    config = Config()
    
    # Walidacja konfiguracji
    if not config.validate():
        print("[BŁĄD] Nieprawidłowa konfiguracja email")
        return False
    
    # Użyj podanego odbiorcy lub domyślnego z konfiguracji
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
        
        # Tworzenie połączenia SMTP
        print(f"[EMAIL] Łączenie z {config.SMTP_SERVER}:{config.SMTP_PORT}...")
        
        # Użyj połączenia SSL (port 465)
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, context=context) as server:
            # Logowanie
            print(f"Logowanie jako {config.EMAIL_SENDER}...")
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            
            # Wysyłanie emaila
            print(f"Wysyłanie emaila do {to_email}...")
            server.send_message(message)
            
        print("[OK] Email wysłany pomyślnie!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("[BŁĄD] Błąd uwierzytelniania. Sprawdź email i hasło.")
        return False
    except smtplib.SMTPException as e:
        print(f"[BŁĄD] Wystąpił błąd SMTP: {e}")
        return False
    except Exception as e:
        print(f"[BŁĄD] Błąd podczas wysyłania emaila: {e}")
        return False


def create_smtp_connection() -> Optional[smtplib.SMTP_SSL]:
    """
    Tworzy i zwraca połączenie SMTP.
    
    Zwraca:
        Obiekt połączenia SMTP lub None w przypadku błędu
    """
    config = Config()
    
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, context=context)
        server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
        return server
    except Exception as e:
        print(f"[BŁĄD] Nie udało się utworzyć połączenia SMTP: {e}")
        return None


def validate_email_config() -> bool:
    """
    Waliduje konfigurację email przed wysłaniem.
    
    Zwraca:
        True jeśli konfiguracja jest poprawna, False w przeciwnym razie
    """
    config = Config()
    return config.validate()


def send_test_email() -> bool:
    """
    Wysyła testowy email w celu weryfikacji konfiguracji.
    
    Zwraca:
        True jeśli testowy email został wysłany pomyślnie, False w przeciwnym razie
    """
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1 style="color: #667eea;">🎉 Email Testowy</h1>
        <p>To jest email testowy z Twojego systemu Newslettera.</p>
        <p>Jeśli to otrzymałeś, Twoja konfiguracja email działa poprawnie!</p>
        <hr>
        <p style="color: #999; font-size: 12px;">Wysłano z Systemu Newslettera</p>
    </body>
    </html>
    """
    
    return send_email(
        subject="System Newslettera - Email Testowy",
        html_content=test_html
    )


if __name__ == "__main__":
    # Test wysyłania emaila
    print("[EMAIL] Test Nadawcy Email Newslettera")
    print("=" * 50)
    
    # Walidacja konfiguracji
    if validate_email_config():
        print("[OK] Konfiguracja email jest poprawna")
        
        # Pytanie użytkownika czy wysłać email testowy
        response = input("\nWysłać email testowy? (t/n): ")
        if response.lower() == 't' or response.lower() == 'y':
            if send_test_email():
                print("\n[OK] Email testowy wysłany pomyślnie!")
            else:
                print("\n[BŁĄD] Nie udało się wysłać emaila testowego")
    else:
        print("[BŁĄD] Konfiguracja email jest niepoprawna")
        print("\nSprawdź plik .env i upewnij się że:")
        print("  - EMAIL_SENDER jest ustawiony")
        print("  - EMAIL_PASSWORD jest ustawiony")
        print("  - EMAIL_RECIPIENT jest ustawiony")
