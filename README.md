# System Automatycznego Newslettera

Projekt ten to kompleksowy system automatyzacji newslettera, który agreguje najważniejsze informacje z kategorii: Świat, Polska, Technologie, Nauka oraz Finanse. Aplikacja generuje estetyczne raporty HTML i dystrybuuje je pocztą elektroniczną każdego ranka.

## 🚀 Funkcjonalności

- **Wiadomości ze Świata**: BBC (Top Stories & World)
- **Wiadomości z Polski**: Gazeta Wyborcza (Kraj)
- **Wiadomości Ekonomiczne**: Bankier.pl (Najważniejsze informacje)
- **Finanse**: Stooq.pl (Złoto, Srebro, Kursy Walut)
- **Email HTML**: Responsywny i estetyczny szablon emaila.

## 📂 Struktura Projektu

```text
Newsletter/
├── newsletter_app.py           # Skonsolidowana wersja programu (wszystko w jednym pliku)
├── src/                        # Kod źródłowy (wersja modułowa)
│   ├── main.py                 # Główny punkt wejścia
│   ├── config.py               # Konfiguracja i zmienne środowiskowe
│   ├── email_sender.py         # Obsługa wysyłania emaili
│   ├── html_template.py        # Generator HTML
│   └── scrapers/               # Moduły pobierające dane
│       ├── world_news.py       # Wiadomości ze świata (BBC)
│       ├── polish_news.py      # Wiadomości z Polski (Gazeta Wyborcza)
│       ├── bankier_news.py     # Wiadomości ekonomiczne (Bankier.pl)
│       └── financial_news.py   # Dane finansowe (Stooq)
├── .env                        # Plik konfiguracyjny (nie udostępniany w repozytorium)
├── .gitignore                  # Pliki ignorowane przez Git
├── requirements.txt            # Zależności Python
└── README.md                   # Dokumentacja projektu
```

## 🛠️ Wymagania

- Python 3.9+

### Zależności Python
Wszystkie wymagane biblioteki znajdują się w pliku `requirements.txt`:
- `requests`
- `yfinance`
- `beautifulsoup4`
- `feedparser`
- `python-dotenv`

## ⚙️ Instalacja i Konfiguracja

1. **Sklonuj repozytorium** (lub pobierz pliki).

2. **Zainstaluj zależności**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Skonfiguruj plik `.env`**:
   Stwórz plik `.env` w głównym katalogu i uzupełnij go swoimi danymi:
   ```env
   # Konfiguracja Email (SMTP)
   SMTP_SERVER=poczta.o2.pl
   SMTP_PORT=465
   EMAIL_SENDER=twoj_email@o2.pl
   EMAIL_PASSWORD=twoje_haslo_aplikacji
   EMAIL_RECIPIENT=adresat@gmail.com
   
   # Strefa czasowa
   TZ=Europe/Warsaw
   ```

## ▶️ Uruchomienie


### Lokalnie (Python)

Aby ręcznie uruchomić generowanie i wysyłkę newslettera:

```bash
python src/main.py
```

