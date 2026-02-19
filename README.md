# 🛏️ Jumia Beddings & Decor Scraper

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-green)
![Requests](https://img.shields.io/badge/Requests-HTTP-orange)
![Status](https://img.shields.io/badge/Project-Portfolio-important)

------------------------------------------------------------------------

## 📌 Project Overview

This project is a **web scraping pipeline** built to extract product
data from the Jumia Nigeria catalog page for:

> **Duvets, Bedsheets, and Pillowcases**

The scraper collects:

-   🏷️ Product Name\
-   💰 New Price Range\
-   🏷️ Old Price Range\
-   ⭐ Number of Ratings

The extracted data is cleaned and exported into a structured **CSV
dataset** for analysis.

------------------------------------------------------------------------

## 🧠 Motivation

The goal of this project was to:

-   Practice real-world web scraping
-   Handle pagination dynamically
-   Structure scraped data properly
-   Implement professional logging practices
-   Prepare for production-grade data pipelines

This project also serves as a foundational step toward building
automated data ingestion systems.

------------------------------------------------------------------------

## ⚙️ Tech Stack

-   **Python 3**
-   `requests` -- for HTTP session handling
-   `BeautifulSoup` -- for HTML parsing
-   `lxml` -- fast HTML parser backend
-   `pandas` -- for data structuring and CSV export
-   `logging` -- for structured event tracking

------------------------------------------------------------------------

## 🏗️ Architecture Overview

### 1️⃣ HTTP Session Handling

A persistent `requests.Session()` object was used to:

-   Improve performance
-   Maintain connection reuse
-   Simulate browser-like interaction

------------------------------------------------------------------------

### 2️⃣ Pagination Handling

The scraper loops through multiple catalog pages:

``` python
for page in range(1, 12):
    url = f"https://www.jumia.com.ng/catalog/?q=duvet+bedsheets+and+pillowcases&page={page}#catalog-listing"
```

This ensures complete extraction across multiple result pages.

------------------------------------------------------------------------

### 3️⃣ Data Extraction Logic

Each product card was targeted using:

``` python
soup.find_all("article", class_="prd _fb col c-prd")
```

From each product container, the following were extracted:

  Field       HTML Class
  ----------- ----------------
  Title       `h3.name`
  New Price   `div.prc`
  Old Price   `div.old`
  Ratings     `div.stars _s`

------------------------------------------------------------------------

### 4️⃣ Data Structuring

Each product was stored as a dictionary:

``` python
store = {
    "Title": ...,
    "New price": ...,
    "Old price": ...,
    "No of stars": ...
}
```

The dictionary was appended to a list and converted into a Pandas
DataFrame:

``` python
best_df = pd.DataFrame(temp_list)
best_df.to_csv("./dataset.csv", index=False)
```

------------------------------------------------------------------------

## 🧾 Logging Implementation

Professional logging was added using Python's `logging` module.

Example:

``` python
import logging

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Connected to Jumia successfully.")
logging.error("Request failed.")
```

### Why Logging Matters

-   Tracks successful page connections
-   Logs request failures
-   Helps debug scraping interruptions
-   Makes the script production-ready

------------------------------------------------------------------------

## 🚨 Challenges Faced

-   Handling mutable dictionary references (avoiding repeated records)
-   Managing missing fields safely using conditional extraction
-   Ensuring clean pagination logic
-   Avoiding duplicated entries

------------------------------------------------------------------------

## 📊 Output Example

  ---------------------------------------------------------------------------
  Title           New Price Rnage         Old Price Range       No of Ratings
  --------------- ----------------- ----------------- -----------------------
  White Golden      ₦ 29,500 - ₦            ₦ 35,000 - ₦         3 out of 5
  Bedsheets And       32,000                  42,000            
  Pillowcases +                                       
  Duvet                                               

  ---------------------------------------------------------------------------

------------------------------------------------------------------------

## 🚀 Future Improvements

-   Add User-Agent headers to reduce bot detection
-   Store data in PostgreSQL instead of CSV
-   Deploy scraper to cloud VM for 24/7 automation
-   Automate execution using cron / GitHub Actions
-   Add data cleaning pipeline for numeric price extraction

------------------------------------------------------------------------

## 📂 Project Structure

    jumia-beddings-scraper/
    │
    ├── scraper.py
    ├── dataset.csv
    ├── scraper.log
    └── README.md

------------------------------------------------------------------------

## 📈 Portfolio Value

This project demonstrates:

-   Web scraping fundamentals
-   HTML DOM parsing
-   Pagination handling
-   Data structuring
-   Logging & monitoring
-   Pipeline thinking

It forms the foundation for larger-scale data engineering workflows.

------------------------------------------------------------------------

## 👤 Author

Built as part of a data engineering portfolio project series.

------------------------------------------------------------------------

⭐ If you found this project interesting, consider giving it a star!
