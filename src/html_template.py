"""
Generator szablonów HTML
Tworzy piękne szablony wiadomości email dla newslettera.
"""

from typing import List, Dict
from datetime import datetime


def generate_newsletter_html(
    world_news: List[Dict],
    polish_news: List[Dict],
    bankier_news: List[Dict],
    financial_data: Dict
) -> str:
    """
    Generuje kompletny newsletter HTML z pobranych danych.
    
    Argumenty:
        world_news: Lista wiadomości ze świata
        polish_news: Lista wiadomości z Polski
        bankier_news: Lista wiadomości z Bankier.pl
        financial_data: Słownik z danymi finansowymi
        
    Zwraca:
        Kompletny ciąg HTML
    """
    current_date = datetime.now().strftime("%d.%m.%Y")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Codzienny Newsletter - {current_date}</title>
        <style>
            {get_css_styles()}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Nagłówek -->
            <div class="header">
                <h1>[NEWS] Codzienny Newsletter</h1>
                <p class="date">{current_date}</p>
            </div>
            
            <!-- Sekcja Wiadomości ze Świata -->
            {create_news_section("[ŚWIAT] Wiadomości ze Świata", world_news, "world")}
            
            <!-- Sekcja Wiadomości z Polski -->
            {create_news_section("[POLSKA] Wiadomości z Polski", polish_news, "poland")}
            
            <!-- Sekcja Wiadomości Bankier.pl -->
            {create_news_section("💰 [FINANSE] Bankier.pl", bankier_news, "finance")}
            
            <!-- Sekcja Finansowa -->
            {create_financial_section(financial_data.get('gold', {}), financial_data.get('silver', {}))}
            
            <!-- Stopka -->
            <div class="footer">
                <p>Newsletter wygenerowany automatycznie</p>
                <p class="small">Dane pobrane: {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def get_css_styles() -> str:
    """
    Pobiera style CSS dla szablonu emaila.
    
    Zwraca:
        Ciąg CSS
    """
    return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .date {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .section {
            padding: 30px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .section:last-of-type {
            border-bottom: none;
        }
        
        .section-title {
            font-size: 24px;
            margin-bottom: 20px;
            color: #333;
            border-left: 4px solid #667eea;
            padding-left: 15px;
        }
        
        .world .section-title { border-left-color: #3498db; }
        .poland .section-title { border-left-color: #e74c3c; }
        .tech .section-title { border-left-color: #9b59b6; }
        .finance .section-title { border-left-color: #f39c12; }
        
        .news-item {
            margin-bottom: 25px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 8px;
            transition: transform 0.2s;
        }
        
        .news-item:hover {
            transform: translateX(5px);
            background-color: #f0f0f0;
        }
        
        .news-item h3 {
            font-size: 18px;
            margin-bottom: 8px;
            color: #2c3e50;
        }
        
        .news-item h3 a {
            color: #2c3e50;
            text-decoration: none;
        }
        
        .news-item h3 a:hover {
            color: #667eea;
        }
        
        .news-meta {
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 8px;
        }
        
        .news-summary {
            font-size: 14px;
            color: #555;
            line-height: 1.5;
        }
        
        .authors {
            font-size: 13px;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 5px;
        }
        
        .financial-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .metal-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .metal-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        
        .metal-price {
            font-size: 32px;
            font-weight: bold;
            color: #27ae60;
            margin: 10px 0;
        }
        
        .metal-change {
            font-size: 14px;
            margin: 5px 0;
        }
        
        .positive {
            color: #27ae60;
        }
        
        .negative {
            color: #e74c3c;
        }
        
        .trends-list {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
        }
        
        .trends-list ul {
            list-style: none;
            padding-left: 0;
        }
        
        .trends-list li {
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .trends-list li:last-child {
            border-bottom: none;
        }
        
        .footer {
            background-color: #34495e;
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .footer .small {
            font-size: 12px;
            opacity: 0.8;
            margin-top: 5px;
        }
        
        .read-more {
            display: inline-block;
            margin-top: 8px;
            color: #667eea;
            text-decoration: none;
            font-size: 13px;
            font-weight: bold;
        }
        
        .read-more:hover {
            text-decoration: underline;
        }
    """


def create_news_section(title: str, news_items: List[Dict], section_class: str) -> str:
    """
    Tworzy sekcję wiadomości z wieloma elementami.
    
    Argumenty:
        title: Tytuł sekcji
        news_items: Lista wiadomości
        section_class: Klasa CSS dla stylizacji
        
    Zwraca:
        Ciąg HTML dla sekcji
    """
    if not news_items:
        return f"""
        <div class="section {section_class}">
            <h2 class="section-title">{title}</h2>
            <p>Brak dostępnych wiadomości.</p>
        </div>
        """
    
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
    
    return f"""
    <div class="section {section_class}">
        <h2 class="section-title">{title}</h2>
        {items_html}
    </div>
    """


def create_scientific_section(title: str, articles: List[Dict]) -> str:
    """
    Tworzy sekcję artykułów naukowych z informacjami o autorach.
    
    Argumenty:
        title: Tytuł sekcji
        articles: Lista artykułów naukowych
        
    Zwraca:
        Ciąg HTML dla sekcji
    """
    if not articles:
        return f"""
        <div class="section science">
            <h2 class="section-title">{title}</h2>
            <p>Brak dostępnych artykułów.</p>
        </div>
        """
    
    items_html = ""
    for article in articles:
        items_html += f"""
        <div class="news-item">
            <h3><a href="{article.get('link', '#')}" target="_blank">{article.get('title', 'Brak tytułu')}</a></h3>
            <div class="news-meta">📚 {article.get('source', 'Nieznane źródło')} • {article.get('published', 'Nieznana data')}</div>
            <div class="authors">👥 {article.get('authors', 'Nieznani autorzy')}</div>
            <div class="news-summary">{article.get('summary', 'Brak abstraktu')}</div>
            <a href="{article.get('link', '#')}" class="read-more" target="_blank">Czytaj publikację →</a>
        </div>
        """
    
    return f"""
    <div class="section science">
        <h2 class="section-title">{title}</h2>
        {items_html}
    </div>
    """


def create_financial_section(gold, silver) -> str:
    """
    Tworzy sekcję danych finansowych z cenami metali szlachetnych.
    
    Argumenty:
        gold: Słownik z danymi złota
        silver: Słownik z danymi srebra
        
    Zwraca:
        Ciąg HTML dla sekcji
    """
    # Karta Złota
    gold_has_error = 'error' in gold
    if gold_has_error:
        gold_html = f"""
        <div class="metal-card">
            <div class="metal-name">⚠️ [ZŁOTO] {gold.get('name', 'Złoto')}</div>
            <div class="news-summary" style="text-align: center; padding: 20px;">
                {gold.get('error', 'Dane tymczasowo niedostępne')}
            </div>
        </div>
        """
    else:
        gold_change_class = 'positive' if gold.get('daily_change', 0) >= 0 else 'negative'
        gold_arrow = '↑' if gold.get('daily_change', 0) >= 0 else '↓'
        currency = gold.get('currency', 'USD')
        symbol = '$' if currency == 'USD' else f' {currency}'
        price_display = f"{symbol}{gold.get('price', 'N/A')}" if currency == 'USD' else f"{gold.get('price', 'N/A')}{symbol}"
        unit_display = f" / {gold.get('unit', '')}" if gold.get('unit') else ""
        
        gold_html = f"""
        <div class="metal-card">
            <div class="metal-name">[ZŁOTO] {gold.get('name', 'Złoto')}</div>
            <div class="metal-price">{price_display}<span style="font-size: 16px; color: #7f8c8d;">{unit_display}</span></div>
            <div class="metal-change {gold_change_class}">
                {gold_arrow} Dziś: {gold.get('daily_change', 0):+.2f} ({gold.get('daily_change_percent', 0):+.2f}%)
            </div>
            <div class="metal-change {gold_change_class}">
                Miesiąc: {gold.get('weekly_change', 0):+.2f} ({gold.get('weekly_change_percent', 0):+.2f}%)
            </div>
        </div>
        """
    
    # Karta Srebra
    silver_has_error = 'error' in silver
    if silver_has_error:
        silver_html = f"""
        <div class="metal-card">
            <div class="metal-name">⚠️ [SREBRO] {silver.get('name', 'Srebro')}</div>
            <div class="news-summary" style="text-align: center; padding: 20px;">
                {silver.get('error', 'Dane tymczasowo niedostępne')}
            </div>
        </div>
        """
    else:
        silver_change_class = 'positive' if silver.get('daily_change', 0) >= 0 else 'negative'
        silver_arrow = '↑' if silver.get('daily_change', 0) >= 0 else '↓'
        currency = silver.get('currency', 'USD')
        symbol = '$' if currency == 'USD' else f' {currency}'
        price_display = f"{symbol}{silver.get('price', 'N/A')}" if currency == 'USD' else f"{silver.get('price', 'N/A')}{symbol}"
        
        silver_html = f"""
        <div class="metal-card">
            <div class="metal-name">[SREBRO] {silver.get('name', 'Srebro')}</div>
            <div class="metal-price">{price_display}</div>
            <div class="metal-change {silver_change_class}">
                {silver_arrow} Dziś: {silver.get('daily_change', 0):+.2f} ({silver.get('daily_change_percent', 0):+.2f}%)
            </div>
            <div class="metal-change {silver_change_class}">
                Miesiąc: {silver.get('weekly_change', 0):+.2f} ({silver.get('weekly_change_percent', 0):+.2f}%)
            </div>
        </div>
        """

    # Trendy (Usunięte zgodnie z prośbą o czyszczenie)
    trends_html = "" # Brak trendów na razie

    section_html = f"""
    <div class="section financial">
        <h2 class="section-title">📊 Rynki Finansowe</h2>
        <div class="financial-grid">
            {gold_html}
            {silver_html}
        </div>
        {trends_html}
    </div>
    """
    return section_html


if __name__ == "__main__":
    # Test generowania szablonu
    test_world = [
        {'title': 'Testowe Wiadomości ze Świata', 'summary': 'Podsumowanie', 'link': '#', 'source': 'BBC', 'published': '2024-01-01'}
    ]
    test_polish = [
        {'title': 'Testowe Wiadomości z Polski', 'summary': 'Podsumowanie', 'link': '#', 'source': 'TVN24', 'published': '2024-01-01'}
    ]
    test_tech = [
        {'title': 'Testowe Wiadomości Tech', 'summary': 'Podsumowanie Tech', 'link': '#', 'source': 'TechCrunch', 'published': '2024-01-01'}
    ]
    test_financial = {
        'gold': {'name': 'Złoto', 'price': 2000, 'daily_change': 10, 'daily_change_percent': 0.5, 'weekly_change': 50, 'weekly_change_percent': 2.5},
        'silver': {'name': 'Srebro', 'price': 25, 'daily_change': -0.5, 'daily_change_percent': -2, 'weekly_change': 1, 'weekly_change_percent': 4},
        'oil': {'name': 'Ropa', 'price': 75.50, 'daily_change': 1.2, 'daily_change_percent': 1.5, 'weekly_change': -2.5, 'weekly_change_percent': -3.2},
        'trends': ['Testowy trend 1', 'Testowy trend 2']
    }
    
    html = generate_newsletter_html(test_world, test_polish, test_tech, test_financial)
    
    # Zapisz do pliku testowego
    with open('test_newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("[OK] Szablon HTML wygenerowany pomyślnie!")
    print("   Zapisano do: test_newsletter.html")
