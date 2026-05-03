import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import urllib.parse
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import SessionLocal
from database.models import CPU

def search_memoryexpress(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.memoryexpress.com/Search/Products?Search={encoded_query}"
    print(f"🔎 Memory Express Search: {query}")
    
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=147)
    
    try:
        driver.get(url)
        time.sleep(7) 
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        items = soup.find_all('div', class_=lambda c: c and ('c-shca-icon-item' in c or 'c-shca-list-item' in c))
        
        for item in items:
            name = ""
            link = ""
            for a_tag in item.find_all('a'):
                if a_tag.text and len(a_tag.text.strip()) > 10:
                    name = a_tag.text.strip()
                    link = "https://www.memoryexpress.com" + a_tag.get('href', '')
                    break
                    
            if not name: continue
            
            pure_name = re.sub(r'[^a-z0-9]', '', name.lower())
            pure_model = re.sub(r'[^a-z0-9]', '', query.split()[-1].lower())
            
            if pure_model not in pure_name: continue 
            if "x3d" not in pure_model and "x3d" in pure_name: continue 
            
            # --- THE REGEX FIX: Capture the whole number including the decimal ---
            price_matches = re.findall(r'\$\s*([\d,]+\.\d{2})', item.text)
            
            if price_matches:
                prices = [float(p.replace(',', '')) for p in price_matches]
                price = min(prices)

                db = SessionLocal()
                try:
                    db.add(CPU(brand="AMD" if "AMD" in name.upper() else "Intel",
                               model_name=name[:100], lowest_price=price,
                               currency='CAD', product_url=link))
                    db.commit()
                    print(f"✅ MemExpress Match: {name[:35]}... @ ${price}")
                    return
                finally:
                    db.close()
                    
        print(f"⚠️ MemExpress: No exact match found for '{query}'")
    except Exception as e:
        print(f"❌ MemExpress Error: {e}")
    finally:
        driver.quit()