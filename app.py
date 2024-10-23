import csv
import requests
from bs4 import BeautifulSoup
import os

def get_book_details(url, soup_book):
    """
    Ici on recupère les détails du livre et on les retourne sous forme de liste
    """
    try:
        title = soup_book.find('h1').text
        upc = soup_book.find_all('td')[0].text
        price_including_tax = soup_book.find_all('td')[3].text.replace('Â', '')
        price_excluding_tax = soup_book.find_all('td')[2].text.replace('Â', '')
        number_available = soup_book.find_all('td')[5].text.replace('In stock (', '').replace(' available)', '')
        review_rating = soup_book.find_all('p', class_='star-rating')[0]['class'][1]
        image_url = soup_book.find('img')['src'].replace('../../', '')
        img_url = url + image_url
        # si la catégorie possède plus d'un mot, on rajoute un espace avant le nom de la catégorie
        category = soup_book.find_all('ul', class_='breadcrumb')[0].find_all('a')[2].text
        if len(category.split()) > 1:
            category = ' ' + category
        div_description = soup_book.find('div', id='product_description')
        description = div_description.find_next('p').text if div_description else "No description available"
        return [title, upc, price_including_tax, price_excluding_tax, number_available, description, review_rating, img_url, category]
    except Exception as e:
        print(f"Erreur lors de la récupération des détails du livre : {e}")
        return None
    
def print_url_images (url, soup_book):
    """
    On récupère les url des images, on les renomme avec le titre du livre et on les télécharhe dans le dossier images
    """
    try:
        image_url = soup_book.find('img')['src'].replace('../../', '')
        img_url = url + image_url
        h1 = soup_book.find('h1').text.replace(' ', '').replace(':', '').replace('/', '').replace('?', '').replace('!', '').replace(';', '').replace(',', '').replace('.', '').replace('\'', '').replace('\"', '').replace('*', '').replace('’', '')
        response = requests.get(img_url)
        # récupérer le nom de la catégorie
        category = soup_book.find_all('ul', class_='breadcrumb')[0].find_all('a')[2].text.replace(' ', '')
        with open(f'{category}/{h1}.jpg', 'wb') as file:
            file.write(response.content)

        
    except Exception as e:
        print(f"Erreur lors de la récupération de l'url de l'image : {e}")
        return None



def process_books_on_page(soup_category, url, writer, number_books):
    """
    Ici on traite les livres sur une page et on les écrit dans le fichier csv
    """
    for i in range(0, number_books + 1):
        try:
            link = soup_category.find_all('h3')[i].find('a')['href']
            url_book = url + 'catalogue/' + link.replace('../', '')
            response_book = requests.get(url_book)
            soup_book = BeautifulSoup(response_book.text, 'html.parser')
            book_details = get_book_details(url, soup_book)
            if book_details:
                writer.writerow([url_book] + book_details)
                
        except IndexError:
            print(f"No more books on this page at index {i}.")
            break
        except Exception as e:
            print(f"Erreur lors du traitement du livre : {e}")
            continue

def process_next_page(soup_category, url_category, url, writer):
    """
    Ici on va traier la page suivante pour plus tard récupérer les livres de cette page
    """
    try:
        next_page = soup_category.find('li', class_='next').find('a')['href']
        url_next_page = url_category.replace('index.html', '') + next_page
        response_category = requests.get(url_next_page)
        soup_category_next = BeautifulSoup(response_category.text, 'html.parser')
        number_books = int(soup_category_next.find('form', class_='form-horizontal').find('strong').text)
        process_books_on_page(soup_category_next, url, writer, number_books)
            
    except Exception as e:
        print(f"Erreur lors de la récupération de la page suivante : {e}")

def scraping_books(url_category, url, writer):
    """
    Ici on va scraper les livres de la catégorie et les écrire dans le fichier csv
    Quand on a fini de traiter une page, on va chercher la page suivante
    Si on ne trouve plus de boutons Next sur la page, on arrête le scraping
    """
    try:
        response_category = requests.get(url_category)
        soup_category = BeautifulSoup(response_category.text, 'html.parser')
        number_books = int(soup_category.find('form', class_='form-horizontal').find('strong').text)
        process_books_on_page(soup_category, url, writer, number_books)

        while soup_category.find('li', class_='next'):
            process_next_page(soup_category, url_category, url, writer)
            next_page = soup_category.find('li', class_='next').find('a')['href']
            url_next_page = url_category.replace('index.html', '') + next_page
            response_category = requests.get(url_next_page)
            soup_category = BeautifulSoup(response_category.text, 'html.parser')
            if not soup_category.find('li', class_='next'):
                print("No more pages to process.")
                break
    except Exception as e: 
        print(f"Erreur générale lors du scraping : {e}")


if __name__ == "__main__":
    """
    On va scrapper les livres de chaque catégorie et les écrire dans un fichier csv nommé avec le nom de la catégorie en faisant une boucle
    On va aussi créer un dossier pour chaque catégorie et télécharger les images des livres dans ces dossiers
    Si un dossier est déjà existant, on va supprimer les fichiers précédents.
    """
    url = 'https://books.toscrape.com/'
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find_all('ul', class_='nav nav-list')
    number_categories = len(categories[0].find_all('a'))
    for i in range(1, number_categories):
        link = categories[0].find_all('a')[i]['href']  
        url_category = url + link
        category = categories[0].find_all('a')[i].text
        category = ''.join(e for e in category if e.isalnum())
        print(category)
        with open(f'{category}.csv', 'w', newline='', encoding='utf8') as fichier_csv:
            writter = csv.writer(fichier_csv)
            writter.writerow(['product_page_url', 'title', 'upc', 'prince_including_tax', 'prince_excluding_tax', 'number_available', 'product_description', 'review_rating', 'image_url', 'category'])
            if not os.path.exists(f'{category}'):
                os.makedirs(f'{category}')
            else:
                for file in os.listdir(f'{category}'):
                    os.remove(f'{category}/{file}')
            scraping_books(url_category, url, writter)
