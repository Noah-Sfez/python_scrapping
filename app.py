from bs4 import BeautifulSoup
import csv
import requests
    

with open('book.csv', 'w', newline='', encoding='utf8') as fichier_csv:
    """
    Ici on va récupérer les informations des livres de la page d'accueil du site
    D'abord je récupère les liens des livres de la page d'accueil
    Ensuite je récupère les informations des livres sur leur page respective
    Et enfin j'écris les informations dans un fichier csv
    """

    writter = csv.writer(fichier_csv)
    url = 'https://books.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('div', class_='image_container')
    link = books[0].find('a')['href']
    url_book = url + link
    response_book = requests.get(url_book)
    soup_book = BeautifulSoup(response_book.text, 'html.parser')

    # Récupération des informations des livres
    title = soup_book.find('h1').text
    upc = soup_book.find_all('td')[0].text
    price_including_tax = soup_book.find_all('td')[3].text.replace('Â', '')
    price_excluding_tax = soup_book.find_all('td')[2].text.replace('Â', '')
    number_available = soup_book.find_all('td')[5].text
    review_rating = soup_book.find_all('td')[6].text
    image_url = soup_book.find('img')['src']
    category = soup_book.find_all('ul', class_='breadcrumb')[0].find_all('a')[2].text
    # Récupération de la description
    div_description = soup_book.find('div', id='product_description')
    description = div_description.find_next('p').text
    # J'écris les informations dans le csv
    writter.writerow(['product_page_url','title', 'upc', 'prince_including_tax', 'prince_excluding_tax', 'number_available', 'product_description', 'review_rating', 'image_url', 'category'])
    writter.writerow([ url_book, title, upc, price_including_tax, price_excluding_tax, number_available, description, review_rating, image_url, category])
    



