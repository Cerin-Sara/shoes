import random
import time
from bs4 import BeautifulSoup
from lxml import etree as et
from csv import writer
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
main_url = "https://www.nike.com/in/w/shoes-3rauvz5e1x6znik1zy7ok"
driver.get(main_url)
time.sleep(5)


def get_dom(base_url):
    driver.get(base_url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, 'html.parser')
    dom = et.HTML(str(product_soup))
    return dom


height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if height == new_height:
        break
    height = new_height

current_url = driver.current_url
page_dom = get_dom(current_url)
product_links = page_dom.xpath('//a[@class="product-card__link-overlay"]/@href')


def gettitle(current_dom):
    try:
        title = current_dom.xpath('//h1[@id="pdp_product_title"]')[0].text
    except Exception as e:
        title = "Title not available"
    return title


def getgender(current_dom):
    try:
        gen = current_dom.xpath('//h2[@class="headline-5 pb1-sm d-sm-ib"]')[0].text.split("'")[0]
    except Exception as e:
        gen = "Gender not available"
    return gen


def getprice(current_dom):
    try:
        price = current_dom.xpath('//div[@data-test="product-price"]')[0].text.split(':')[1].replace(u'\u20B9', '')
    except Exception as e:
        price = "Price not available"
    return price


def getdescription(current_dom):
    try:
        desc = current_dom.xpath('//div[@class="description-preview body-2 css-1pbvugb"]/p/text()')[0]
    except Exception as e:
        desc = "Description not available"
    return desc


def getcolor(current_dom):
    try:
        color = current_dom.xpath('//div[@class="description-preview body-2 css-1pbvugb"]/ul/li/text()')[0].split(':')[1]
    except Exception as e:
        color = "Color not available"
    return color


def getstylecode(current_dom):
    try:
        style = current_dom.xpath('//div[@class="description-preview body-2 css-1pbvugb"]/ul/li/text()')[1].split(':')[1]
    except Exception as e:
        style = "Style code not available"
    return style


def getstarrating(current_dom):
    try:
        star = current_dom.xpath('//p[@class="d-sm-ib pl4-sm"]/text()')[0]
    except:
        star = "Star rating not available"
    return star


def getreviews(current_dom):
    try:
        reviews = current_dom.xpath('//h3[@class="headline-4 css-xd87ek"]/span/text()')[0].split(' ')[1].replace('(', '').replace(')', '')
    except Exception as e:
        reviews = "Review not available"
    return reviews


with open('nike_shoe_data.csv', 'w', newline='', encoding='utf-8') as f:
    theWriter = writer(f)
    heading = ['Product link', 'Product title', 'Gender', 'Sales price', 'Color', 'Style code', 'No of reviews',
               'Star rating', 'Description']
    theWriter.writerow(heading)
    for product in product_links:
        product_link = product
        product_dom = get_dom(product_link)
        product_title = gettitle(product_dom)
        gender = getgender(product_dom)
        if (gender != "Gender not available") and (gender != "Men") and (gender == "Women"):
            gender = "Unisex"
        sale_price = getprice(product_dom)
        description = getdescription(product_dom)
        color = getcolor(product_dom)
        style_code = getstylecode(product_dom)
        star_rating = getstarrating(product_dom)
        no_of_reviews = getreviews(product_dom)
        record = [product_link, product_title, gender, sale_price, color, style_code, no_of_reviews, star_rating, description]
        theWriter.writerow(record)
        time.sleep(random.randint(3, 5))

