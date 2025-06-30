import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time

BASE_URL = 'https://tuwroclaw.com'
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
OUTPUT_FILE = 'articles.json'
REQUEST_DELAY = 0.5

# Pobieranie strony i zwracanie obiektu BeautifulSoup
def fetch(path):
    try:
        resp = requests.get(BASE_URL + path, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, 'html.parser')
    except Exception as e:
        return None

# Pobieranie listy artykułów z sekcji wiadomości
def get_article_list():
    soup = fetch('/wiadomosci/')
    if not soup:
        return []
    
    cards = soup.select('div.news-card')
    out = []
    for c in cards:
        # Link do artykułu
        a = c.find('a')
        href = a['href'] if a and 'href' in a.attrs else None    
        if not href:
            continue
        # Data publikacji
        date_el = c.select_one('.news-card__date')
        raw_date = (date_el.text.strip() if date_el else '')
        date_iso = datetime.strptime(raw_date, '%Y/%m/%d').strftime('%Y-%m-%d')

        out.append({
            'url': href,
            'date': date_iso
        })
    return out

def get_article_details(path):
    soup = fetch(path)
    if not soup:
        return {}
    
    ## Tytuł artykułu
    title_el = soup.select_one('h1.news__title')
    title = title_el.text.strip() if title_el else ''

    ## Data publikacji
    date_el = soup.select_one('span.news__date')
    date = date_el.text.strip() if date_el else ''

    ## Lead artykułu
    lead_el = soup.select_one('p.news__lead')
    lead = lead_el.text.strip() if lead_el else ''

    ## Treść artykułu
    content_nodes = soup.select('div.news__content p, div.news__content ul li')
    paragraphs = []
    for p in content_nodes:
        text = p.get_text(strip=True)
        if text:
            paragraphs.append(text)
    ## Czasami lead jest w div content a czasem poza nim 
    ## więc go usuwamy jeśli jest w pierwszym paragrafie
    if lead == paragraphs[0]:
        paragraphs.pop(0)
    content = "\n\n".join(paragraphs)

    return {
        'title': title,
        'date': date,
        'lead': lead,
        'content': content,
    }

def main():
    today_iso = datetime.today().date().isoformat()
    articles_index = get_article_list()
    results = []

    # Chcemy tylko dzisiejsze artykuły
    todays_articles = [art for art in articles_index if art['date'] == today_iso]

    for art in todays_articles:
        details = get_article_details(art['url'])
        if details:
            entry = {
                'url': BASE_URL + art['url'],
                **details
            }
            results.append(entry)
        time.sleep(REQUEST_DELAY)

    # Zapis do JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Zapisano {len(results)} artykułów (z datą {today_iso}) do pliku {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
