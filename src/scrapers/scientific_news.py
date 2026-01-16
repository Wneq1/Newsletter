"""
Skraper Artykułów Naukowych
Pobiera 3 najważniejsze artykuły naukowe związane z metrologią, elektroniką i technologią.
"""

import feedparser
import requests
from typing import List, Dict
from datetime import datetime, timedelta


def fetch_scientific_articles() -> List[Dict[str, str]]:
    """
    Pobiera 3 najważniejsze artykuły naukowe związane z metrologią, elektroniką i technologią.
    
    Zwraca:
        Lista słowników zawierających informacje o artykułach z kluczami:
        - title: Tytuł artykułu
        - summary: Abstrakt lub opis
        - link: Link do pełnego artykułu
        - source: Źródło publikacji
        - authors: Autorzy artykułu
        - published: Data publikacji
    """
    articles = []
    
    # Kategorie arXiv dla elektroniki i instrumentacji
    arxiv_categories = [
        'physics.ins-det',  # Instrumentacja i Detektory
        'eess.SP',          # Przetwarzanie Sygnałów
        'cs.SY',            # Systemy i Sterowanie
    ]
    
    # Przeszukiwanie arXiv
    for category in arxiv_categories:
        try:
            url = f'http://export.arxiv.org/rss/{category}'
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:3]:
                # Wyodrębnienie autorów
                authors = ', '.join([author.name for author in entry.get('authors', [])])
                if not authors:
                    authors = entry.get('author', 'Nieznany')
                
                article = {
                    'title': entry.get('title', 'Brak tytułu'),
                    'summary': entry.get('summary', 'Brak dostępnego abstraktu')[:300] + '...',
                    'link': entry.get('link', ''),
                    'source': 'arXiv',
                    'authors': authors,
                    'published': entry.get('published', 'Nieznana data')
                }
                
                # Filtrowanie po słowach kluczowych
                if is_relevant_article(article):
                    articles.append(article)
                    
        except Exception as e:
            print(f"[OSTRZEŻENIE] Błąd pobierania z kategorii arXiv {category}: {e}")
            continue
    
    # Spróbuj także IEEE Xplore RSS (jeśli dostępne)
    try:
        ieee_url = 'https://ieeexplore.ieee.org/rss/TOC23.XML'  # Instrumentation and Measurement
        feed = feedparser.parse(ieee_url)
        
        for entry in feed.entries[:2]:
            article = {
                'title': entry.get('title', 'Brak tytułu'),
                'summary': entry.get('summary', entry.get('description', 'Brak abstraktu'))[:300],
                'link': entry.get('link', ''),
                'source': 'IEEE Xplore',
                'authors': entry.get('author', 'IEEE'),
                'published': entry.get('published', 'Nieznana data')
            }
            articles.append(article)
    except Exception as e:
        print(f"[OSTRZEŻENIE] Błąd pobierania z IEEE: {e}")
    
    # Zwróć 3 najbardziej trafne
    return rank_by_relevance(articles)[:3]


def is_relevant_article(article: Dict) -> bool:
    """
    Sprawdza, czy artykuł jest związany z metrologią, elektroniką lub pomiarami.
    
    Argumenty:
        article: Słownik artykułu
        
    Zwraca:
        True jeśli jest trafny, False w przeciwnym razie
    """
    keywords = [
        'metrology', 'metrolog', 'measurement', 'pomiar',
        'electronics', 'elektronik', 'sensor', 'czujnik',
        'instrumentation', 'instrument', 'calibration', 'kalibracja',
        'signal processing', 'przetwarzanie sygnału',
        'data acquisition', 'akwizycja danych'
    ]
    
    text = (article['title'] + ' ' + article['summary']).lower()
    
    return any(keyword in text for keyword in keywords)


def rank_by_relevance(articles: List[Dict]) -> List[Dict]:
    """
    Ranguje artykuły według trafności dla metrologii i elektroniki.
    
    Argumenty:
        articles: Lista artykułów
        
    Zwraca:
        Posortowana lista według trafności
    """
    # Prosta punktacja oparta na dopasowaniach słów kluczowych
    priority_keywords = ['metrology', 'metrolog', 'measurement', 'electronics']
    
    def score_article(article):
        text = (article['title'] + ' ' + article['summary']).lower()
        return sum(1 for keyword in priority_keywords if keyword in text)
    
    return sorted(articles, key=score_article, reverse=True)


if __name__ == "__main__":
    # Test skrapera
    print("[NAUKA] Pobieranie artykułów naukowych...")
    articles = fetch_scientific_articles()
    
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Autorzy: {article['authors']}")
        print(f"   Źródło: {article['source']}")
        print(f"   Link: {article['link']}")
