"""
Skraper wiadomości ze świata
Pobiera 3 najważniejsze wiadomości ze świata z międzynarodowych kanałów RSS.
"""

import feedparser
from typing import List, Dict


def fetch_world_news() -> List[Dict[str, str]]:
    """
    Pobiera 3 najważniejsze wiadomości ze świata wyłącznie z BBC (Top Stories oraz World).
    
    Zwraca:
        Lista słowników zawierających wiadomości z kluczami:
        - title: Tytuł wiadomości
        - summary: Krótki opis
        - link: Link do pełnego artykułu
        - source: Nazwa źródła wiadomości
        - published: Data publikacji
    """
    news_sources = [
        {
            'url': 'http://feeds.bbci.co.uk/news/rss.xml', # Top Stories
            'name': 'BBC Info'
        },
        {
            'url': 'http://feeds.bbci.co.uk/news/world/rss.xml', # World
            'name': 'BBC World'
        }
    ]
    
    all_news = []
    seen_links = set()
    
    for source in news_sources:
        try:
            feed = feedparser.parse(source['url'])
            # Pobierz nieco więcej, aby po deduplikacji zostało wystarczająco dużo
            for entry in feed.entries[:5]:
                link = entry.get('link', '')
                
                # Prosta deduplikacja po linku
                if link in seen_links:
                    continue
                seen_links.add(link)

                news_item = {
                    'title': entry.get('title', 'Brak tytułu'),
                    'summary': entry.get('summary', entry.get('description', 'Brak dostępnego podsumowania')),
                    'link': link,
                    'source': source['name'],
                    'published': entry.get('published', 'Nieznana data')
                }
                all_news.append(news_item)
        except Exception as e:
            print(f"[OSTRZEŻENIE] Błąd pobierania z {source['name']}: {e}")
            continue
    
    # Zwróć 3 najlepsze unikalne wiadomości
    return all_news[:3]


def parse_rss_feed(url: str) -> List[Dict]:
    """
    Parsuje kanał RSS i wyciąga wiadomości.
    
    Argumenty:
        url: URL kanału RSS
        
    Zwraca:
        Lista sparsowanych wiadomości
    """
    try:
        feed = feedparser.parse(url)
        return feed.entries
    except Exception as e:
        print(f"Błąd parsowania kanału RSS {url}: {e}")
        return []


def filter_and_rank_news(items: List[Dict]) -> List[Dict]:
    """
    Filtruje i rankuje wiadomości według trafności i aktualności.
    
    Argumenty:
        items: Lista wiadomości
        
    Zwraca:
        Przefiltrowana i posortowana lista
    """
    # Na razie zwracam elementy bez zmian
    # Można dodać bardziej zaawansowany ranking później
    return items


if __name__ == "__main__":
    # Test skrapera
    print("[ŚWIAT] Pobieranie wiadomości ze świata...")
    news = fetch_world_news()
    
    for i, item in enumerate(news, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   Źródło: {item['source']}")
        print(f"   Link: {item['link']}")
