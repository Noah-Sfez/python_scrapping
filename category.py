import csv
import requests
from bs4 import BeautifulSoup


with open('category.csv', 'w', newline='', encoding='utf8') as fichier_csv:
    writter = csv.writer(fichier_csv)
    url = 'https://books.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find_all('ul', class_='nav nav-list')
    link = categories[0].find_all('a')[4]['href']
    url_category = url + link
    response_category = requests.get(url_category)
    soup_category = BeautifulSoup(response_category.text, 'html.parser')
    number_books = int(soup_category.find('form', class_='form-horizontal').find('strong').text)
    writter.writerow(['product_page_url', 'title', 'upc', 'prince_including_tax', 'prince_excluding_tax', 'number_available', 'product_description', 'review_rating', 'image_url', 'category'])
    for i in range(0, number_books + 1):
        # Récupération des liens des livres
        try : 
            link = soup_category.find_all('h3')[i].find('a')['href']
            url_book = url + 'catalogue/' + link.replace('../', '')               
            print(url_book)
            print(i)
            i += 1
            response_book = requests.get(url_book)
            soup_book = BeautifulSoup(response_book.text, 'html.parser')
            title = soup_book.find('h1').text
            upc = soup_book.find_all('td')[0].text
            price_including_tax = soup_book.find_all('td')[3].text.replace('Â', '')
            price_excluding_tax = soup_book.find_all('td')[2].text.replace('Â', '')
            number_available = soup_book.find_all('td')[5].text.replace('In stock (', '').replace(' available)', '')
            review_rating = soup_book.find_all('p', class_='star-rating')[0]['class'][1]
            image_url = soup_book.find('img')['src'].replace('../../', '')
            img_url = url + image_url
            category = soup_book.find_all('ul', class_='breadcrumb')[0].find_all('a')[2].text
            div_description = soup_book.find('div', id='product_description')
            description = div_description.find_next('p').text
            writter.writerow([url_book, title, upc, price_including_tax, price_excluding_tax, number_available, description, review_rating, img_url, category])
        except IndexError:
            next_page = soup_category.find('li', class_='next').find('a')['href']
            url_next_page = url_category.replace('index.html', '') + next_page
            response_category = requests.get(url_next_page)
            soup_category2 = BeautifulSoup(response_category.text, 'html.parser')
            number_books = int(soup_category2.find('form', class_='form-horizontal').find('strong').text)
            books_restant = number_books - i
            for i in range(0, books_restant + 1):
                try : 
                    link2 = soup_category2.find_all('h3')[i].find('a')['href']
                    url_book = url + 'catalogue/' + link2.replace('../', '')
                    print(url_book)
                    print(i)
                    i += 1
                    response_book = requests.get(url_book)
                    soup_book = BeautifulSoup(response_book.text, 'html.parser')
                    title = soup_book.find('h1').text
                    upc = soup_book.find_all('td')[0].text
                    price_including_tax = soup_book.find_all('td')[3].text.replace('Â', '')
                    price_excluding_tax = soup_book.find_all('td')[2].text.replace('Â', '')
                    number_available = soup_book.find_all('td')[5].text.replace('In stock (', '').replace(' available)', '')
                    review_rating = soup_book.find_all('p', class_='star-rating')[0]['class'][1]
                    image_url = soup_book.find('img')['src'].replace('../../', '')
                    img_url = url + image_url
                    category = soup_book.find_all('ul', class_='breadcrumb')[0].find_all('a')[2].text
                    div_description = soup_book.find('div', id='product_description')
                    description = div_description.find_next('p').text
                    writter.writerow([url_book, title, upc, price_including_tax, price_excluding_tax, number_available, description, review_rating, img_url, category])
                except IndexError:
                    print('fini')
            i = 0
            break
            
        except Exception as e:
            print(e)
            continue

        
    
    

    