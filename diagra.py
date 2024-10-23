import matplotlib.pyplot as plt
import csv
import os

def get_books_data():
    """
    Ici on va récupérer le nombre de livres par catégorie et le prix moyen des livres par catégorie
    """
    number_books_by_category = {}
    total_price_by_category = {}
    
    for file in os.listdir('csv'):
        if file.endswith('.csv'):
            category = file.replace('.csv', '')
            total_price = 0
            number_books = 0
            
            with open(f'csv/{file}', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        
                        price = float(row['prince_including_tax'].replace('£', ''))
                        total_price += price
                        number_books += 1
                    except ValueError:
                       
                        continue
            
            if number_books > 0:
                number_books_by_category[category] = number_books
                total_price_by_category[category] = total_price / number_books  

    return number_books_by_category, total_price_by_category

def plot_books_pie_chart(data):
    """
    Crée un diagramme en camembert représentant la proportion de livres par catégorie
    """
    categories = list(data.keys())
    number_books = list(data.values())

    # Créer un diagramme en camembert
    plt.figure(figsize=(10, 10))
    plt.pie(number_books, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Pourcentage de livres par catégorie')
    plt.show()

def plot_average_price_bar_chart(data):
    """
    Crée un graphique en barres représentant le prix moyen des livres par catégorie
    """
    categories = list(data.keys())
    average_prices = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categories, average_prices, color='skyblue')
    plt.xlabel('Catégories')
    plt.ylabel('Prix moyen (£)')
    plt.title('Prix moyen des livres par catégorie')
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout()  
    plt.show()

if __name__ == "__main__":
    number_books_by_category, average_price_by_category = get_books_data()
    
    plot_books_pie_chart(number_books_by_category)
    
    plot_average_price_bar_chart(average_price_by_category)
