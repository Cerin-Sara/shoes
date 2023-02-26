from bs4 import BeautifulSoup
from lxml import etree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from csv import writer
import random
import time

base_url = "https://www.adidas.co.in"
product_list = []


driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(base_url)


def get_dom(url):
    """
    Get the page source as a BeautifulSoup object, then convert to an lxml ET object.
    """
    driver.get(url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, "html.parser")
    dom = ET.HTML(str(product_soup))
    return dom


page_url = "https://www.adidas.co.in/men%7Cunisex%7Cwomen-shoes"
while(1):
    page_dom = get_dom(page_url)
    page_products_link = page_dom.xpath('//a[@class="glass-product-card__assets-link"]/@href')
    product_list += page_products_link
    next_page_url = page_dom.xpath('//a[@data-auto-id="plp-pagination-next"]/@href')
    if next_page_url:
        page_url = base_url+next_page_url[0]
    else:
        break
    time.sleep(random.randint(3, 5))


def get_title(current_dom):
    try:
        product_title = current_dom.xpath('//h1[@class="name___120FN"]/span/text()')[0]
    except Exception as e:
        product_title = 'No title available'
    return product_title


def get_cat_and_gender(current_dom):
    try:
        cat_and_gen = current_dom.xpath('//div[@data-auto-id="product-category"]/span/text()')[0]
    except Exception as e:
        cat_and_gen = "Not found"
    return cat_and_gen


def get_saleprice(current_dom):
    try:
        price = current_dom.xpath('//div[@class="gl-price-item notranslate"]/text()')[0].replace(u'\u20B9', '')
    except Exception as e:
        price = current_dom.xpath('//div[@class="gl-price-item gl-price-item--sale notranslate"]/text()')[0].replace(u'\u20B9', '')
    return price


def get_starrating(current_dom):
    try:
        rating = current_dom.xpath('//div[@class="ratings-label-container___13pr-"]/span')[0].text
    except Exception as e:
        rating = "Rating not available"
    return rating


def get_reviews(current_dom):
    try:
        reviews = current_dom.xpath('//h2[@class="accordion-title___2sTgR"]')[-1].text.split(' ')[1][1:-1]
    except Exception as e:
        reviews = "Review not available"
    return reviews


def get_desc(current_dom):
    try:
        desc = current_dom.xpath('//div[@class="text-content___13aRm"]/p')[0].text
    except Exception as e:
        desc = "Description not available"
    return desc


def get_details(current_dom):
    try:
        details = current_dom.xpath('//div[@class="bullets___3bsSs"]/ul/li')
        detail_list = [detail.text for detail in details]
    except Exception as e:
        detail_list = "No details available"
    return detail_list


def get_code(current_dom):
    try:
        code = current_dom.xpath('//div[@class="bullets___3bsSs"]/ul/li')[-1].text
    except Exception as e:
        code = "Code not available"
    return code


def get_color(current_dom):
    try:
        color = current_dom.xpath('//div[@class="bullets___3bsSs"]/ul/li')[-2].text
    except Exception as e:
        color = "Color not available"
    return color


with open('adidas_shoe_data.csv', 'w', newline='', encoding='utf-8') as f:
    theWriter = writer(f)
    heading = ['Product link', 'Product code', 'Product title', 'Category', 'Gender', 'Color', 'Sale Price', 'Star rating',
              'No of reviews', 'Description', 'Details']
    theWriter.writerow(heading)
    for product in product_list:
        product_link = base_url+product
        product_dom = get_dom(product_link)
        title = get_title(product_dom)
        category_and_gender = get_cat_and_gender(product_dom)
        if category_and_gender == "Not found":
            category = "Category not available"
            gender = "Gender not available"
        elif(len(category_and_gender.split(' '))==3):
            category = category_and_gender.split(' ')[2]
            gender = category_and_gender.split(' ')[0]
        else:
            category = category_and_gender
            gender = "Unisex"
        sale_price = get_saleprice(product_dom)
        star_rating = get_starrating(product_dom)
        no_of_reviews = get_reviews(product_dom)
        description = get_desc(product_dom)
        product_details = get_details(product_dom)
        product_code = get_code(product_dom)
        product_color = get_color(product_dom)
        record = [product_link, product_code, title, category, gender, product_color, sale_price, star_rating, no_of_reviews,
                  description, product_details]
        theWriter.writerow(record)
        time.sleep(random.randint(3, 5))
driver.quit()

