import schedule
import time
from Scrappers.Utilidades import *

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
    for url in urls:
        print(f"Starting Pccomponentes scraping for {url}...")
        data = scrape_pccomponentes(url)
        subir_datos(data)
        print(f"Pccomponentes scraping done for {url}.")

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
    # Run the jobs once immediately
    # job_vastai()
    job_pccomponentes()
    # job_luz()
    # job_wallapop()
    

    # Schedule the jobs
    schedule.every(2.5).minutes.do(job_vastai)
    # schedule.every().day.at("19:00").do(job_pccomponentes)
    schedule.every(15).minutes.do(job_pccomponentes)
    schedule.every(15).minutes.do(job_wallapop)
    schedule.every().hour.do(job_luz)  # Schedule job_luz to run every hour

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()