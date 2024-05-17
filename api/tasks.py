import os
import json
import time
import uuid
from celery import shared_task
from bs4 import BeautifulSoup
from selenium import webdriver

def parse_product_info(driver, url):
    driver.get(url)
    time.sleep(4)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_name = soup.find('span', class_='cmp-product-details-main__heading-title').text.strip()
    description_div = soup.find('div', class_='cmp-product-details-main__description')
    product_description = description_div.find('p').text.strip() if description_div.find('p') else description_div.text.strip()

    nutrition_summary = soup.find('ul', class_='cmp-nutrition-summary__heading-primary')
    if nutrition_summary:
        nutrients = nutrition_summary.find_all('li', class_='cmp-nutrition-summary__heading-primary-item')
        calories = nutrients[0].find_all('span', class_='sr-only sr-only-pd')[1].text.strip()
        fats = nutrients[1].find_all('span', class_='sr-only sr-only-pd')[1].text.strip()
        carbs = nutrients[2].find_all('span', class_='sr-only sr-only-pd')[1].text.strip()
        proteins = nutrients[3].find_all('span', class_='sr-only sr-only-pd')[1].text.strip()
    else:
        calories = fats = carbs = proteins = None

    nutrition_details = soup.find('div', class_='cmp-nutrition-summary__details-column-view-mobile')
    if nutrition_details:
        details_items = nutrition_details.find_all('li', class_='label-item')
        additional_fats = details_items[0].find('span', class_='value').find_all('span')[0].text.strip().replace('\n', '')
        sugar = details_items[1].find('span', class_='value').find_all('span')[0].text.strip().replace('\n', '')
        salt = details_items[2].find('span', class_='value').find_all('span')[0].text.strip().replace('\n', '')
        portion = details_items[3].find('span', class_='value').find_all('span')[0].text.strip().replace('\n', '')
    else:
        additional_fats = sugar = salt = portion = None

    unique_id = str(uuid.uuid4())

    return {
        'uuid': unique_id,
        'name': product_name,
        'description': product_description,
        'calories': calories,
        'fats': fats,
        'carbs': carbs,
        'proteins': proteins,
        'additional_fats': additional_fats,
        'sugar': sugar,
        'salt': salt,
        'portion': portion
    }

@shared_task
def parse_mcdonalds_menu():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote(
        command_executor='http://seleniums:4444/wd/hub',
        options=options
    )

    url = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_links = []
    for item in soup.find_all('li', class_='cmp-category__item'):
        link = item.find('a', class_='cmp-category__item-link')['href']
        product_links.append(link)
    
    products_info = []
    for link in product_links:
        product_info = parse_product_info(driver, f"https://www.mcdonalds.com{link}")
        if product_info:
            products_info.append(product_info)
    
    save_path = 'data'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    json_file = os.path.join(save_path, 'mcdonalds_menu.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(products_info, f, ensure_ascii=False, indent=4)
    
    driver.quit()
    