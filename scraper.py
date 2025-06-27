import requests
from bs4 import BeautifulSoup
import datetime

def get_list_of_articles():
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
    return news_items

def articles_list():
    news_list = get_list_of_articles()
    articles_list = [] # dodać potem dane do struktury czy coś
    for item in news_list:
        
        # Pobierz link
        link = item.find('a')
        article_url = 'https://tuwroclaw.com' + link['href'] if link else '#'
        
        # Pobierz tytuł
        title = item.find('h3', class_='news-card__title')
        title_text = title.text.strip() if title else 'Brak tytułu'

        # Pobierz kategorię
        category = item.find('span', class_='label label--cat')
        category_text = category.text.strip() if category else 'Brak kategorii'
        
        # Pobierz datę
        date = item.find('div', class_='news-card__date')
        date_text = date['datetime'] if date and 'datetime' in date.attrs else date.text.strip() if date else datetime.date.today().strftime('%Y-%m-%d')        

        print(f"Tytuł: {title_text}")
        print(f"Kategoria: {category_text}")
        print(f"Data: {date_text}")
        print(f"Link: {article_url}")
        print("-" * 40)

def articles_details():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    news_list = get_list_of_articles()
    for item in news_list:
        
        # Pobierz link
        link = item.find('a')
        article_url = 'https://tuwroclaw.com' + link['href'] if link else '#'

        article_response = requests.get(article_url, headers=headers)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        # Pobierz tytuł
        title = article_soup.find('h1', class_='news__title')
        title_text = title.text.strip() if title else 'Brak tytułu'

        # Pobierz kategorię
        category = item.find('span', class_='label label--cat')
        category_text = category.text.strip() if category else 'Brak kategorii'
        
        content_list= []

        # Pobierz lead
        lead = article_soup.find('p', class_='news__lead')
        lead_text = lead.text.strip() if lead else ""
        content_list.append(lead_text)
        
        # Pobierz resztę artykułu
        content = article_soup.find('div', class_='news__content')
        content_sections = content.find_all('p')
        for section in content_sections:
            # Wywalamy tekst z odnośników
            if section.find('a', href=True):
                continue
            text = section.get_text(strip=True)
            if text:
                content_list.append(section.text)
        
        content_text = "\n\n".join(content_list)

        # Pobierz datę
        date = article_soup.find('span', class_='news__date')
        date_text = date.text.strip()       

        print(f"Tytuł: {title_text}")
        print(f"Kategoria: {category_text}")
        print(f"Data: {date_text}")
        print(f"Link: {article_url}")
        print(f"Treść: \n {content_text}")
        print("-" * 40)

articles_details()
