from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from urllib.request import urlopen
import mysql.connector

mydb = mysql.connector.connect(host="localhost",user="USERNAME",passwd="PASSWORD",database="DATABASE")
mycursor = mydb.cursor(buffered=True)

def get_product(page):
    # specify the url
    quote_page = page
    # query the website and return the html to the variable page
    page = urlopen(quote_page)
    # parse the html using beautiful soup and store in variable soup
    soup = BeautifulSoup(page, "html.parser")

    # Take out the <div> of name and get its value
    #url = soup.find("link",  itemprop="url")
    site_name = soup.find("meta",  property="og:site_name")
    url = soup.find("meta",  property="og:url")
    title = soup.find("meta",  property="og:title")
    currency = soup.find("meta",  property="og:price:currency")
    image = soup.find("meta",  property="og:image")
    image_secure = image = soup.find("meta",  property="og:image:secure_url")

    gtin = soup.find("meta",  itemprop="gtin13")
    brand = soup.find("meta",  itemprop="name")
    description = soup.find("meta",  itemprop="description")
    category = soup.find("meta",  itemprop="category")
    category = category["content"]
    category = category.strip() # strip() is used to remove starting and trailing


    #url = soup.find("meta",  itemprop="mainEntityOfPage url")
    #availability = soup.find("meta",  itemprop="availability")
    #availability = (availability["content"]).replace("https://schema.org/", "")
    for available in soup.find_all('div', attrs={'id':'availability'}):
        #print availability .find('span')
        availability = available .find('title')
        availability = availability.text
        availability = availability.strip() # strip() is used to remove starting and trailing
        #print availability

    priceCurrency = soup.find("meta",  itemprop="priceCurrency")
    sku = soup.find("meta",  itemprop="sku")
    price = soup.find("meta",  itemprop="price")
    #prices = price.text.strip() # strip() is used to remove starting and trailing
    price2 = soup.find("meta",  property="og:price:amount")

    print(url["content"] if url else "No meta title given")
    print(title["content"] if url else "No meta title given")
    print(availability if availability else "No meta title given")
    print(priceCurrency["content"] if priceCurrency else "No meta title given")
    #print(price["content"] if price else "No meta title given")
    print(price2["content"] if price else "No meta title given")
    print(sku["content"] if price else "No meta title given")
    print(image["content"] if price else "No meta title given")
    print(brand["content"] if price else "No meta title given")
    print(description["content"] if price else "No meta title given")
    print(category if category else "No meta title given")

   # NEW SECTION
    vUrl = (url["content"] if url else "No meta title given")
    vTitle = (title["content"] if url else "No meta title given")
    print(vUrl)
    print(vTitle)
    vAvailability = (availability if availability else "No meta title given")
    print(vAvailability)
    vPriceCurrency = (priceCurrency["content"] if priceCurrency else "No meta title given")
    vPrice = (price2["content"] if price else "No meta title given")
    vSKU = (sku["content"] if price else "No meta title given")
    vImage = (image["content"] if price else "No meta title given")
    vBrand = (brand["content"] if price else "No meta title given")
    vDescription = (description["content"] if price else "No meta title given")
    vCategory = (category if category else "No meta title given")


    sql = "INSERT INTO stage_jbhifi(SKU, Title, Brand, Availability, PriceCurrency, Price, URL, ImageURL, Description, Category) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s,%s ) ON DUPLICATE KEY UPDATE Title=%s,Brand=%s,Availability=%s,PriceCurrency=%s,Price=%s,URL= %s,ImageURL=%s,Description = %s,Category = %s"
    #sql = "INSERT INTO stage_jbhifi(SKU, Title, Brand, Availability, PriceCurrency, Price, URL, ImageURL, Description, Category) VALUES (1,1,1,1,1,1,1,1,1,1)"
    val = (vSKU, vTitle, vBrand, vAvailability,vPriceCurrency,vPrice,vUrl,vImage,vDescription,vCategory, vTitle, vBrand, vAvailability,vPriceCurrency,vPrice,vUrl,vImage,vDescription,vCategory)
    print("Status Updated")
    mycursor.execute(sql,val)

    mydb.commit()



    # get the index price
    price_box = soup.find("div", attrs={"class":"price"})
    price = price_box



def get_sitemap(url):
    get_url = requests.get(url)

    if get_url.status_code == 200:
        return get_url.text
    else:
        print('Unable to fetch sitemap: %s.' % url)


def process_sitemap(s):
    soup = BeautifulSoup(s, 'lxml')
    result = []

    for loc in soup.findAll('loc'):
        result.append(loc.text)

    return result


def is_sub_sitemap(url):
    parts = urlparse(url)
    if parts.path.endswith('.xml') and 'sitemap' in parts.path:
        return True
    else:
        return False


def parse_sitemap(s):
    sitemap = process_sitemap(s)
    result = []

    while sitemap:
        candidate = sitemap.pop()

        if is_sub_sitemap(candidate):
            sub_sitemap = get_sitemap(candidate)
            for i in process_sitemap(sub_sitemap):
                sitemap.append(i)
        else:
            result.append(candidate)

    return result


def main():
    sitemap = get_sitemap('https://www.jbhifi.com.au/sitemap.xml') 

    url_count = 0
    for url in parse_sitemap(sitemap):

        #url_count += 1

        if "https://www.jbhifi.com.au/products/" in url:
            url_count += 1
            print("%5d) %s" % (url_count, url))
            try:
                get_product(url)
            except Exception:
                pass

    print("-end-of-list-")


if __name__ == '__main__':
    main()
