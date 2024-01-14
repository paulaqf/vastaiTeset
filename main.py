import schedule
import time
from Scrappers.Utilidades import *
import concurrent.futures

# URLs to scrape
urls_pccomponentes = [
    "https://www.pccomponentes.com/discos-duros/1-tb/conexiones-m-2/disco-ssd?seller=pccomponentes",
    "https://www.pccomponentes.com/procesadores/amd-ryzen-9/intel-i7/intel-i9?seller=pccomponentes",
    "https://www.pccomponentes.com/tarjetas-graficas/geforce-rtx-4090-series?seller=pccomponentes",
    "https://www.pccomponentes.com/placas-base/socket-am5?seller=pccomponentes",
    "https://www.pccomponentes.com/memorias-ram/64-gb/ddr5?seller=pccomponentes",
    "https://www.pccomponentes.com/refrigeracion-liquida/kit-refrigeracion-liquida/socket-am5?seller=pccomponentes"
]

urls_wallapop = [
    {"https://es.wallapop.com/app/search?filters_source=quick_filters&keywords=rtx%204090&latitude=40.96427&longitude=-5.66385&order_by=price_low_to_high&min_sale_price=1250", "4090"},
]

def job_vastai(gpu):
    try:
        print("Starting Vastai scraping on " + gpu +"...")
        data = scrape_vastai(gpu)
        subir_datos(data)
        print("Vastai scraping done.")
    except Exception as e:
        print(f"An error occurred in job_vastai: {e}")

def job_pccomponentes(parallel_execution):
    def process_url(url):
        try:
            print(f"Starting Pccomponentes scraping for {url}...")
            data = scrape_pccomponentes(url)
            subir_datos(data)
            print(f"Pccomponentes scraping done for {url}.")
        except Exception as e:
            print(f"An error occurred in process_url for {url}: {e}")

    if parallel_execution:
        # Create a ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Process each URL in parallel
            executor.map(process_url, urls_pccomponentes)
    else:
        # Process each URL sequentially
        for url in urls_pccomponentes:
            process_url(url)

def job_luz():
    try:
        print("Starting Luz scraping...")
        data = scrape_luz()
        subir_datos(data)
        print("Luz scraping done.")
    except Exception as e:
        print(f"An error occurred in job_luz: {e}")

def job_wallapop():
    try:
        print("Starting Wallapop scraping...")
        for url, product in urls_wallapop:
            data = scrape_wallapop(url, product)
            subir_datos(data)
        print("Wallapop scraping done.")
    except Exception as e:
        print(f"An error occurred in job_wallapop: {e}")

def main():
    # Run the jobs once immediately
    job_vastai("4090")
    job_vastai("3090")
    job_pccomponentes(True)
    job_luz()
    job_wallapop()

    # Schedule the jobs
    schedule.every(2.5).minutes.do(job_vastai, "4090")
    schedule.every(2.5).minutes.do(job_vastai, "3090")
    schedule.every(10).minutes.do(job_pccomponentes, True)
    schedule.every(10).minutes.do(job_wallapop)
    schedule.every().hour.do(job_luz)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()