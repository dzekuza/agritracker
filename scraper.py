import requests
from bs4 import BeautifulSoup
import schedule
import time

# 1. Scrape wheat prices
def fetch_wheat_prices():
    print("🔍 Fetching wheat prices...")
    url = "https://www.agritel.com/en/home"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    wheat_cells = soup.select('table:has(th:-soup-contains("Wheat (€/t)")) tbody tr td')
    wheat_data = [td.get_text(strip=True) for td in wheat_cells]

    prices = []
    for i in range(0, len(wheat_data), 4):
        if i + 2 < len(wheat_data):
            prices.append({
                "month": wheat_data[i],
                "price": wheat_data[i + 1],
                "change": wheat_data[i + 2]
            })
        if len(prices) == 5:
            break

    return prices

def fetch_corn_prices():
    print("🔍 Fetching corn prices...")
    url = "https://www.agritel.com/en/home"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    corn_cells = soup.select('table:has(th:-soup-contains("Corn (€/t)")) tbody tr td')
    corn_data = [td.get_text(strip=True) for td in corn_cells]

    prices = []
    for i in range(0, len(corn_data), 4):
        if i + 2 < len(corn_data):
            prices.append({
                "month": corn_data[i],
                "price": corn_data[i + 1],
                "change": corn_data[i + 2]
            })
        if len(prices) == 5:
            break

    return prices

def fetch_rapeseed_prices():
    print("🔍 Fetching rapeseed prices...")
    url = "https://www.agritel.com/en/home"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    rape_cells = soup.select('table:has(th:-soup-contains("Rapeseed (€/t)")) tbody tr td')
    rape_data = [td.get_text(strip=True) for td in rape_cells]

    prices = []
    for i in range(0, len(rape_data), 4):
        if i + 2 < len(rape_data):
            prices.append({
                "month": rape_data[i],
                "price": rape_data[i + 1],
                "change": rape_data[i + 2]
            })
        if len(prices) == 5:
            break

    return prices

# 2. Send data to WordPress
def send_to_wp_wheat_eu(data):
    print("📤 Sending data to WordPress (wheat_eu)...")
    url = "https://mediumslateblue-wildcat-124558.hostingersite.com/wp-json/wp/v2/wheat_eu"
    auth = ("admin", "3S3K Sx1Y rIs5 hFLT wc09 rybR")  # replace with actual credentials
    headers = {"Content-Type": "application/json"}

    for item in data:
        payload = {
    "title": item["month"],
    "status": "publish",
    "acf": {
        "month": item["month"],
        "price": item["price"],
        "change": item["change"]
    }
}

        res = requests.post(url, auth=auth, headers=headers, json=payload)

        if res.status_code == 201:
            print(f"✅ Created: {item['month']}")
        else:
            print(f"❌ Error {res.status_code}: {res.text}")

# 3. Job to run every minute
def job():
    print("⏳ Running scheduled task...")
    wheat_prices = fetch_wheat_prices()
    # send_to_wp_wheat_eu(wheat_prices)
    requests.post("http://localhost:5000/api/update")

# 4. Scheduler
schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    print("🚀 Agritracker started. Running every minute...")
    job()  # Run immediately on start

    while True:
        schedule.run_pending()
        time.sleep(1)