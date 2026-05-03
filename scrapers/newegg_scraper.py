import requests
from bs4 import BeautifulSoup
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import SessionLocal
from database.models import CPU

def scrape_newegg_cad_precision(url):
    # Ensure we are actually hitting the .ca domain
    url = url.replace(".com", ".ca")
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    print(f"🕵️  Scraping Newegg Canada: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Using the exact DIV structure you found in the inspect tool
        price_div = soup.find('div', class_='price-current')
        
        if price_div:
            dollars = price_div.find('strong').text.replace(',', '').strip()
            cents = price_div.find('sup').text.strip()
            
            final_price_cad = float(f"{dollars}{cents}")
            
            print(f"✅ Found the Native CAD Price! -> ${final_price_cad}")

            db = SessionLocal()
            try:
                new_cpu = CPU(
                    brand='AMD',
                    model_name="AMD Ryzen 7 7800X3D",
                    lowest_price=final_price_cad,
                    currency='CAD', # <--- Set this back to CAD
                    product_url=url
                )
                # Cleanup old USD entry if it exists to avoid dashboard clutter
                db.query(CPU).filter(CPU.product_url.contains("newegg")).delete()
                
                db.add(new_cpu)
                db.commit()
                print(f"🚀 Database Updated with Native CAD!")
            finally:
                db.close()
        else:
            print("⚠️ Could not find price DIV. Newegg.ca layout might differ slightly.")

    except Exception as e:
        print(f"❌ Scraper error: {e}")

if __name__ == "__main__":
    # Test with the CA link
    test_url = "https://www.newegg.ca/amd-ryzen-7-7800x3d-ryzen-7-7000-series/p/N82E16819113793"
    scrape_newegg_cad_precision(test_url)