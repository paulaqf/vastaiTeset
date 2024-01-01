from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import requests
import json
from urllib.parse import urlparse, unquote
import time

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")


def scrape_pccomponentes(url):
    # Parse the URL to get the component type
    parsed_url = urlparse(unquote(url))
    component_type = parsed_url.path.split('/')[1]

    print(f"Scraping {component_type}...")

    # Initialize the webdriver
    driver = webdriver.Chrome(options=options)  # Make sure you have the Firefox driver in your PATH

    # Navigate to the new URL
    print("     - Opening browser...")
    driver.get(url)

    # Wait until the page is fully loaded
    wait = WebDriverWait(driver, 10)
    print("     - Waiting for page to load...")

    # Try to locate the cookie notice by its XPath and click on it if it exists
    try:
        cookie_notice = wait.until(EC.element_to_be_clickable((By.ID, 'cookiesAcceptAll')))
        cookie_notice.click()
    except:
        pass

    # Wait for the product grid to be present
    products = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="product-grid"]/div/a')))

    # Initialize an empty list to store the product data
    product_list = []

    # Loop through each product

    for product in products:
        # Extract the product name and price using XPath selectors
        product_name = product.find_element(By.XPATH, './/div/div[1]/div[2]/h3').text
        product_price_text = product.find_element(By.XPATH, './/div/div[1]/div[2]/div[1]').text

        # Split the price string into lines, replace the comma with a dot, remove non-digit characters and convert to float
        price_list = [float(price.replace('.','').replace('€', '').replace(',', '.')) for price in product_price_text.split('\n') if price]

        # If there's more than one price, select the lowest one
        if len(price_list) > 1:
            product_price = min(price_list)
        elif price_list:
            product_price = price_list[0]
        else:
            product_price = None  # Or some default value

        # Save the product name and price in a dictionary and append it to the list
        product_list.append({"Nombre": product_name, "Precio": product_price})

    driver.quit()
    print("     - Browser closed.")

    return {component_type: product_list}


def scrape_vastai():
    # Define the URL of the webpage
    url = "https://cloud.vast.ai/"
    # Create a new instance of the Firefox driver
    print("Opening browser...")
    driver = webdriver.Chrome(options=options)

    # Go to the URL
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".machine-row")))

    # Wait for the dropdowns to be present
    dropdowns = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormControl-root.css-vc1rr1")))

    # Select the last dropdown
    dropdown = dropdowns[-1]
    dropdown.click()

    # Wait for the dropdown menu to open and then select 'Price(inc.)'
    price_inc_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[@data-value='price-asc']")))
    price_inc_option.click()

    # Wait for the page to update after selecting the dropdown value
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".machine-row")))

    # Refresh the dropdowns
    dropdowns = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormControl-root.css-vc1rr1")))

    # Select the second dropdown
    dropdown = dropdowns[1]
    dropdown.click()

    # Wait for the dropdown menu to open and then select 'RTX 4090'
    rtx_4090_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[@data-value='RTX 4090']")))
    time.sleep(1)
    rtx_4090_option.click()
    time.sleep(5)

    # Get the HTML of the webpage
    html = driver.page_source

    # Create a BeautifulSoup object with the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the div elements with the class 'fixed-layout' in the BeautifulSoup object
    fixed_layouts = soup.find_all('div', class_='fixed-layout')

    # Define the keys for the dictionary
    keys = ["Localization", "GPU", "TFLOPs", "MachineID", "HOST", "Verified", "VRAM", "GPUSpeed", "Motherboard", "PCIeSpeed", "PCIe", "CPU", "CPUSpeed", "RAM", "Disk", "DiskSize", "DiskSpeed", "UploadSpeed", "DownloadSpeed", "Ports", "DLPerf", "MaxCUDA", "Price"]

    # For each fixed layout, find all child divs with the class 'abspos popover-container', find the 'button-hover' div, extract the text from its child 'abspos MuiBox-root css-0' div, and create a dictionary
    data = [dict(zip(keys, [div.text.strip() for div in fixed_layout.find_all('div', class_='abspos popover-container')] + [round(float(fixed_layout.find_next_sibling('div', class_='button-hover').find('div', class_='abspos MuiBox-root css-0').text.strip().replace('$', '').replace('/hr', '')), 3)])) for fixed_layout in fixed_layouts]
    #
    print("Closing browser...")
    driver.quit()
    return {"maquinas": data}

def scrape_wallapop():
    url = "https://es.wallapop.com/app/search?filters_source=quick_filters&keywords=rtx%204090&latitude=40.96427&longitude=-5.66385&order_by=price_low_to_high&min_sale_price=1250"

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    try:
        reject_cookies_button = wait.until(EC.presence_of_element_located((By.ID, 'onetrust-reject-all-handler')))
        reject_cookies_button.click()
    except:
        pass

    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'body > tsl-root > tsl-public > div > div > tsl-search > div > tsl-search-layout > div > div:nth-child(2) > div:nth-child(1) > tsl-public-item-card-list > div > a')))

    product_list = []

    for product in products:
        product_name = product.find_element(By.CSS_SELECTOR, 'div div div p').text
        product_price_text = product.find_element(By.CSS_SELECTOR, '.ItemCard__price.ItemCard__price--bold').text
        product_price = float(product_price_text.replace('€', '').replace('.', '').replace(',', '.').strip())
        try:
            product.find_element(By.CSS_SELECTOR, 'tsl-svg-icon[src="/assets/icons/item-card/reserved.svg"]')
            product_reserved = True
        except:
            product_reserved = False

        if "4090" in product_name and not product_reserved:
            product_list.append({"Nombre": product_name, "Precio": product_price})

    driver.quit()

    return {"GPU-wallapop": product_list}

def scrape_luz():
    # Define the URL of the webpage
    url = "https://tarifaluzhora.es/"

    # Initialize the webdriver
    driver = webdriver.Chrome(options=options)  # Make sure you have the Firefox driver in your PATH

    # Navigate to the URL
    driver.get(url)

    # Wait until the page is fully loaded
    wait = WebDriverWait(driver, 10)

    # Try to locate the kWh price by its XPath and extract it
    try:
        price_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="block-agrippa-content"]/article/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/span')))
        price_text = price_element.text
    except:
        price_text = None

    driver.quit()

    # Extract the numeric price from the text
    if price_text is not None:
        price = float(price_text.replace(' €/kWh', '').strip())
    else:
        price = None  # Or some default value

    # Define UTC+1 timezone
    utc_plus_one = timezone(timedelta(hours=1))

    # Get the current time in UTC+1
    timestamp = datetime.now(utc_plus_one).isoformat()
    luz = {"precio": price, "timestamp": timestamp}

    return {"luz": luz}

def subir_datos(data):
    # Define UTC+1 timezone
    utc_plus_one = timezone(timedelta(hours=1))

    for key in data:
        if isinstance(data[key], list):
            for item in data[key]:
                if isinstance(item, dict):
                    item['timestamp'] = datetime.now(utc_plus_one).isoformat()

    # Convert the data to a JSON string
    data_json = json.dumps(data)
    print(data_json)
    # Send a POST request with the data
    print("Sending data...")
    response = requests.post('https://datos.montanera.pro/scrapingVastai', data=data_json)

    # Check the status of the request
    if response.status_code == 200:
        print("Data sent successfully")
    else:
        print("Failed to send data, status code:", response.status_code)




