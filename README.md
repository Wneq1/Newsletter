# System Automatycznego Newslettera

Projekt ten to zautomatyzowany system newslettera, który zbiera wiadomości z różnych źródeł (wiadomości ze świata, z Polski, technologie, nauka oraz finanse), formatuje je w atrakcyjny email HTML i wysyła codziennie rano.

## 🚀 Funkcjonalności

- **Wiadomości ze Świata**: BBC, Al Jazeera, NYT (Top 3)
- **Wiadomości z Polski**: Polskie Radio, TVN24, Onet (Top 3)
- **Technologie**: TechCrunch, The Verge, Wired (Top 3)
- **Nauka**: Artykuły z arXiv oraz IEEE Xplore filtrowane pod kątem metrologii i elektroniki.
- **Finanse**: Aktualne ceny złota i srebra (PLN) wraz z historią zmian (dzienną i miesięczną).
- **Email HTML**: Responsywny i estetyczny szablon emaila.

## 📂 Struktura Projektu

```
Newsletter/
├── src/                        # Kod źródłowy
│   ├── main.py                 # Główny punkt wejścia
│   ├── config.py               # Konfiguracja i zmienne środowiskowe
│   ├── email_sender.py         # Obsługa wysyłania emaili
│   ├── html_template.py        # Generator HTML
│   └── scrapers/               # Moduły pobierające dane
│       ├── world_news.py       # Wiadomości ze świata
│       ├── polish_news.py      # Wiadomości z Polski
│       ├── tech_news.py        # Technologie
│       ├── scientific_news.py  # Nauka
│       └── financial_news.py   # Finanse (Złoto/Srebro)
├── .env                        # Plik konfiguracyjny (nie udostępniany w repozytorium)
├── .gitignore                  # Pliki ignorowane przez Git
├── requirements.txt            # Zależności Python
├── Dockerfile                  # Konfiguracja obrazu Docker
├── docker-compose.yml          # Konfiguracja Docker Compose
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

## 📝 Autor

Projekt stworzony przy użyciu asysty AI.
