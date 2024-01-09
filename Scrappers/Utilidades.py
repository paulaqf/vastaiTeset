from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import requests
import json
from urllib.parse import urlparse, unquote
import time

options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("window-size=1400,1500")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537")

def scrape_pccomponentes(url):
    # Parse the URL to get the component type
    parsed_url = urlparse(unquote(url))
    component_type = parsed_url.path.split('/')[1]

    print(f"Scraping {component_type}...")

    # Initialize the webdriver
    driver = webdriver.Firefox(options=options)

    # Navigate to the new URL
    print(f"     - Opening browser {component_type}...")
    driver.get(url)

    # Wait until the page is fully loaded
    wait = WebDriverWait(driver, 10)
    

    # # Try to locate the cookie notice by its XPath and click on it if it exists
    # print("     - Esperando cookies...")
    # try:
    #     cookie_notice = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, 'cookiesAcceptAll')))
    #     driver.execute_script("arguments[0].style.border='3px solid red'", cookie_notice)  # Highlight the element
    #     cookie_notice.click()
    #     print("     - Cookies aceptadas.")
    # except:
    #     print("     - No hay cookies.")
    #     pass

    # Wait for the product grid to be present
    product_grid = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'product-grid')))
    driver.execute_script("arguments[0].style.border='3px solid red'", product_grid)  # Highlight the element
    
    
    print(f"     - Browser {component_type} closed.")

    print("     - Extrayendo datos...")

    # Select all div children of the product grid
    products = product_grid.find_elements(By.TAG_NAME, 'a')
    print(f"     - {len(products)} productos encontrados.")

    # Initialize an empty list to store the product data
    product_list = []
    # Loop through each product

    for product in products:
        # Extract the product name and price from the data attributes
        product_name = product.get_attribute('data-product-name')
        product_price = float(product.get_attribute('data-product-price'))

        # Save the product name and price in a dictionary and append it to the list
        product_list.append({"Nombre": product_name, "Precio": product_price})
    print(product_list)

    driver.quit()

    return {component_type: product_list}


def scrape_wallapop(url, producto_buscar):
    driver = webdriver.Firefox(options=options)
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

        if producto_buscar in product_name and not product_reserved:
            product_list.append({"Nombre": product_name, "Precio": product_price})

    driver.quit()

    return {"GPU-wallapop": product_list}


def scrape_vastai():


    # Define the URL of the webpage
    url = "https://cloud.vast.ai/"
    # Create a new instance of the Firefox driver
    print("  -Opening Vastai browser...")
    driver = webdriver.Firefox(options=options)

    # Go to the URL
    driver.get(url)
    # Wait for the dropdowns to be present
    dropdowns = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormControl-root.css-vc1rr1")))
    time.sleep(5)
    # Esperar a que se carguen las máquinas
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".results-table")))
    # driver.execute_script("arguments[0].style.border='3px solid red'",driver.find_element(By.CSS_SELECTOR, ".results-table"))  # Highlight the element


    # Select the last dropdown
    dropdown = dropdowns[-1]
    driver.execute_script("arguments[0].style.border='3px solid red'", dropdown)  # Highlight the element

    # Wait until the overlaying element is no longer present or visible
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBackdrop-root.MuiBackdrop-invisible.MuiModal-backdrop.css-esi9ax")))

    dropdown.click()
     # Wait for the dropdown menu to open and then select 'Price(inc.)'
    price_inc_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-value='price-asc']")))
    driver.execute_script("arguments[0].style.border='3px solid red'", price_inc_option)  # Highlight the element

    price_inc_option.click()
    driver.execute_script("arguments[0].style.border='3px solid green'", price_inc_option)  # Highlight the element



    # Refresh the dropdowns
    dropdowns = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormControl-root.css-vc1rr1")))
    # Select the second dropdown
    dropdown = dropdowns[1]
    driver.execute_script("arguments[0].style.border='3px solid red'", dropdown)  # Highlight the element

    time.sleep(2)
    dropdown.click()
    driver.execute_script("arguments[0].style.border='3px solid green'", dropdown)  # Highlight the element


    # Wait for the dropdown menu to open and then select 'RTX 4090'
    rtx_4090_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-value='RTX 4090']")))
    driver.execute_script("arguments[0].style.border='3px solid red'", rtx_4090_option)  # Highlight the element


    rtx_4090_option.click()
    # Wait for the content to update
    time.sleep(3)

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



def scrape_luz():
    # Define the URL of the webpage
    url = "https://tarifaluzhora.es/"

    # Initialize the webdriver
    driver = webdriver.Firefox(options=options)

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




