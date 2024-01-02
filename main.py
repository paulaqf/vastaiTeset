import schedule
import time
from Scrappers.Utilidades import *
import concurrent.futures

# URLs to scrape
urls = [
    "https://www.pccomponentes.com/discos-duros/1-tb/conexiones-m-2/disco-ssd?seller=pccomponentes",
    "https://www.pccomponentes.com/procesadores/amd-ryzen-9/intel-i7/intel-i9?seller=pccomponentes",
    "https://www.pccomponentes.com/tarjetas-graficas/geforce-rtx-4090-series?seller=pccomponentes",
    "https://www.pccomponentes.com/placas-base/socket-am5?seller=pccomponentes",
    "https://www.pccomponentes.com/memorias-ram/64-gb/ddr5?seller=pccomponentes",
    "https://www.pccomponentes.com/refrigeracion-liquida/kit-refrigeracion-liquida/socket-am5?seller=pccomponentes"
]

def job_vastai():
    print("Starting Vastai scraping...")
    data = scrape_vastai()
    subir_datos(data)
    print("Vastai scraping done.")

def job_pccomponentes():
    def process_url(url):
        print(f"Starting Pccomponentes scraping for {url}...")
        data = scrape_pccomponentes(url)
        subir_datos(data)
        print(f"Pccomponentes scraping done for {url}.")

    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Process each URL in parallel
        executor.map(process_url, urls)

def job_luz():
    print("Starting Luz scraping...")
    data = scrape_luz()
    subir_datos(data)
    print("Luz scraping done.")

def job_wallapop():
    print("Starting Wallapop scraping...")
    data = scrape_wallapop()
    subir_datos(data)
    print("Wallapop scraping done.")

def main():
    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Run the jobs once immediately
        executor.submit(job_vastai)
        # executor.submit(job_pccomponentes)
        # executor.submit(job_luz)
        # executor.submit(job_wallapop)

        # Schedule the jobs
        schedule.every(2.5).minutes.do(executor.submit, job_vastai)
        schedule.every(15).minutes.do(executor.submit, job_pccomponentes)
        schedule.every(15).minutes.do(executor.submit, job_wallapop)
        schedule.every().hour.do(executor.submit, job_luz)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    main()