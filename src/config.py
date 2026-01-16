"""
Moduł zarządzania konfiguracją
Ładuje i waliduje zmienne środowiskowe dla systemu newslettera.
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()


class Config:
    """Klasa konfiguracyjna dla systemu newslettera."""
    
    # Konfiguracja Email
    SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'poczta.o2.pl')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '465'))
    EMAIL_SENDER: str = os.getenv('EMAIL_SENDER', '')
    EMAIL_PASSWORD: str = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_RECIPIENT: str = os.getenv('EMAIL_RECIPIENT', '')
    
    # Strefa czasowa
    TIMEZONE: str = os.getenv('TZ', 'Europe/Warsaw')
    
    # Opcjonalne klucze API
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY', None)
    
    @classmethod
    def validate(cls) -> bool:
        """
        Waliduje czy cała wymagana konfiguracja jest obecna.
        
        Zwraca:
            bool: True jeśli konfiguracja jest poprawna, False w przeciwnym razie
        """
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
            print("Sprawdź plik .env")
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
        print(f"  OpenAI API: {'Skonfigurowano' if cls.OPENAI_API_KEY else 'Nie skonfigurowano'}")


def get_config() -> Config:
    """
    Pobiera instancję konfiguracji.
    
    Zwraca:
        Config: Obiekt konfiguracji
    """
    return Config()


if __name__ == "__main__":
    # Test konfiguracji
    config = get_config()
    config.display_config()
    
    if config.validate():
        print("[OK] Konfiguracja jest poprawna!")
    else:
        print("[BŁĄD] Konfiguracja jest niepoprawna!")
