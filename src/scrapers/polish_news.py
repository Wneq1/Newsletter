"""
Skraper wiadomości z Polski
Pobiera 3 najważniejsze wiadomości z polskich źródeł informacyjnych.
"""

import feedparser
from typing import List, Dict
import re


def strip_html_tags(text: str) -> str:
    """
    Usuwa znaczniki HTML i czyści treść tekstową.
    
    Argumenty:
        text: Tekst potencjalnie zawierający HTML
        
    Zwraca:
        Czysty tekst bez znaczników HTML
    """
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
    
    return text.strip()


def fetch_polish_news() -> List[Dict[str, str]]:
    """
    Pobiera 3 najważniejsze wiadomości z polskich źródeł (tylko Gazeta Wyborcza).
    
    Zwraca:
        Lista słowników zawierających wiadomości z kluczami:
        - title: Nagłówek wiadomości
        - summary: Krótki opis (tylko tekst, brak HTML/zdjęć)
        - link: Link do pełnego artykułu
        - source: Nazwa źródła
        - published: Data publikacji
    """
    polish_sources = [
        {
            'url': 'http://rss.gazeta.pl/pub/rss/gazetawyborcza_kraj.xml',
            'name': 'Gazeta Wyborcza - Kraj'
        }
    ]
    
    all_news = []
    
    for source in polish_sources:
        try:
            feed = feedparser.parse(source['url'])
            for entry in feed.entries[:5]:  # Pobierz 5 najlepszych
                # Pobierz podsumowanie i wyczyść je z HTML/zdjęć
                raw_summary = entry.get('summary', entry.get('description', 'Brak opisu'))
                clean_summary = strip_html_tags(raw_summary)
                
                # Ogranicz długość podsumowania
                if len(clean_summary) > 200:
                    clean_summary = clean_summary[:200] + '...'
                
                news_item = {
                    'title': strip_html_tags(entry.get('title', 'Brak tytułu')),
                    'summary': clean_summary,
                    'link': entry.get('link', ''),
                    'source': source['name'],
                    'published': entry.get('published', 'Nieznana data')
                }
                all_news.append(news_item)
        except Exception as e:
            print(f"[OSTRZEŻENIE] Błąd pobierania z {source['name']}: {e}")
            continue
    
    # Zwróć 3 najnowsze
    return all_news[:3]


def parse_polish_rss(url: str) -> List[Dict]:
    """
    Parsuje polski kanał RSS.
    
    Argumenty:
        url: URL kanału RSS
        
    Zwraca:
        Lista sparsowanych wiadomości
    """
    try:
        feed = feedparser.parse(url)
        return feed.entries
    except Exception as e:
        print(f"Błąd parsowania RSS {url}: {e}")
        return []


def filter_polish_news(items: List[Dict]) -> List[Dict]:
    """
    Filtruje wiadomości pod kątem specyficznych polskich treści.
    
    Argumenty:
        items: Lista wiadomości
        
    Zwraca:
        Przefiltrowana lista
    """
    # Można dodać filtrowanie po słowach kluczowych
    return items


if __name__ == "__main__":
    # Test skrapera
    print("[POLSKA] Pobieranie wiadomości z Polski...")
    news = fetch_polish_news()
    
    for i, item in enumerate(news, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   Źródło: {item['source']}")
        print(f"   Link: {item['link']}")
