from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.parse

website_link = "https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as" \
               "-show=on&as=off "
root_url = "https://www.flipkart.com"

response = requests.get(website_link)

soup = BeautifulSoup(response.content, 'html.parser')
response.raise_for_status()

soup_results = soup.findAll('div', class_='_13oc-S')

product_name = []
product_price = []
product_link = []
product_specs = []
product_rating = []
for results in soup_results:
    try:
        name = results.find('div', class_='_4rR01T').get_text()
    except:
        name = 'N/A'
    try:
        price = results.find('div', class_='_30jeq3 _1_WHN1').get_text()
    except:
        price = 'N/A'
    try:
        rating = results.find('div', class_='_3LWZlK').get_text()
    except:
        rating = 'N/A'
    try:
        result_link = results.find('a', class_='_1fQZEK').get('href')
        relative_link = urllib.parse.urljoin(root_url, result_link)
    except:
        relative_link = 'N/A'
    specifications = []
    try:
        specs = results.find('div', class_='fMghEO')
        for each in specs:
            specifications = [x.text for x in each.find_all('li', class_='rgWa7D')]
    except:
        specifications = ['N/A']

    product_name.append(name)
    product_price.append(price)
    product_link.append(relative_link)
    product_specs.append(specifications)
    product_rating.append(rating)

product_overview = pd.DataFrame({"Name": product_name, "Price": product_price, "Product link": product_link, "Product specs": product_specs, "Rating": product_rating})
print(product_overview)
product_overview.to_excel("product_data.xlsx", index=False)
