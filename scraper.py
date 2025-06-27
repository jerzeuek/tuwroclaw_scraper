import requests
from bs4 import BeautifulSoup
import datetime

# Bez headerów 403
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
url = 'https://tuwroclaw.com/wiadomosci/'

# Pobranie zawartości strony z aktualnościami
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Sekcja z wiadomościami
news_section = soup.find('div', class_='list')
if not news_section:
    news_section = soup  # Na wszelki wypadek xD

# Znajdź wszystkie newsy
news_items = news_section.find_all('div', class_='news-card')
for item in news_items:
    # Pobierz tytuł
    title = item.find('h2') or item.find('h3') or item.find('h4')
    title_text = title.text.strip() if title else 'Brak tytułu'
    
    # Pobierz datę
    date = item.find('div', class_='news-card__date')
    date_text = date['datetime'] if date and 'datetime' in date.attrs else date.text.strip() if date else datetime.date.today().strftime('%Y-%m-%d')
    
    # Pobierz link
    link = item.find('a')
    link_url = link['href'] if link else '#'
    
    print(f"Tytuł: {title_text}")
    print(f"Data: {date_text}")
    print(f"Link: {link_url}")
    print("-" * 40)
