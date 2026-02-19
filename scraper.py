import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import logging


temp_list = []
session = requests.Session()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("scraper.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Logger initialized")

for page in range(1,12):
    try:
        url=f"https://www.jumia.com.ng/catalog/?q=duvet+bedsheets+and+pillowcases&page={page}#catalog-listing"
        response = session.get(url, timeout=5)
        response.raise_for_status()
        logger.info(f"Connected to Jumia..Scrapping {page} page data")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            data_list = soup.find_all("article", class_="prd _fb col c-prd")
            for i in data_list:
                store = {}
                old_tag = i.find("div", class_="old")
                title = i.find("h3", class_="name")
                new_price = i.find("div", class_="prc")
                nos = i.find("div", class_="stars _s")

                store["Title"] = title.get_text(strip=True) if title else None
                store["New price"] = new_price.get_text(strip=True) if new_price else None
                store["Old price"] = old_tag.get_text(strip=True) if old_tag else None
                store["No of stars"] = nos.get_text(strip=True) if nos else None
                temp_list.append(store)
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occured trying to get data from page {page} to jumia: {e}")
else:
    logger.info("Scrapping finished.")


best_df = pd.DataFrame(temp_list)
best_df.to_csv("./dataset.csv")

