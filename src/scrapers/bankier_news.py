"""
Skraper wiadomości finansowych z Bankier.pl
Pobiera najważniejsze wiadomości finansowe.
"""

import feedparser
from typing import List, Dict
import re


def strip_html_tags(text: str) -> str:
    """
    Usuwa znaczniki HTML i czyści treść tekstową.
    """
    if not text:
        return ""
    
    # Usuwanie znaczników HTML
    text = re.sub(r'<[^>]+>', '', text)
    
    # Usuwanie nadmiarowych białych znaków
    text = re.sub(r'\s+', ' ', text)
    
    # Dekodowanie encji HTML (podstawowe)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('<![CDATA[', '')
    text = text.replace(']]>', '')
    
    return text.strip()


def fetch_bankier_news() -> List[Dict[str, str]]:
    """
    Pobiera 3 najważniejsze wiadomości z Bankier.pl.
    
    Zwraca:
        Lista słowników zawierających wiadomości z kluczami:
        - title: Nagłówek wiadomości
        - summary: Krótki opis
        - link: Link do pełnego artykułu
        - source: Nazwa źródła
        - published: Data publikacji
    """
    source = {
        'url': 'https://www.bankier.pl/rss/wiadomosci.xml',
        'name': 'Bankier.pl'
    }
    
    all_news = []
    
    try:
        feed = feedparser.parse(source['url'])
        
        for entry in feed.entries[:5]:  # Pobierz 5 najlepszych
            # Pobierz podsumowanie
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

    # Zwróć 3 najnowsze
    return all_news[:3]


if __name__ == "__main__":
    # Test skrapera
    print("[FINANSE] Pobieranie wiadomości z Bankier.pl...")
    news = fetch_bankier_news()
    
    for i, item in enumerate(news, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   Źródło: {item['source']}")
        print(f"   Link: {item['link']}")
