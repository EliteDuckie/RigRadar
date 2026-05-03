import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import SessionLocal
from database.models import CPU

def search_newegg_discovery(query):
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.newegg.ca/p/pl?d={encoded_query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}

    print(f"🔎 Searching Newegg Canada: '{query}'")
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_containers = soup.find_all(class_='price-current')
        
        for p_container in price_containers:
            parent = p_container.find_parent('div', class_=['item-container', 'item-cell'])
            if not parent: continue
            
            title_tag = parent.find('a', class_='item-title')
            strong_tag = p_container.find('strong')
            sup_tag = p_container.find('sup')
            
            if title_tag and strong_tag and sup_tag:
                name = title_tag.text.strip()
                model_num = query.split()[-1].lower()
                name_lower = name.lower()
                if model_num not in name_lower: continue
                if "x3d" not in model_num and "x3d" in name_lower: continue
                link = title_tag['href']
                dollars = strong_tag.text.replace(',', '').strip()
                cents = sup_tag.text.strip().replace('.', '')
                final_price = float(f"{dollars}.{cents}")

                print(f"✅ Newegg Match: {name[:40]}... @ ${final_price}")
                db = SessionLocal()
                try:
                    db.add(CPU(brand="AMD" if "AMD" in name.upper() else "Intel",
                               model_name=name[:100], lowest_price=final_price,
                               currency='CAD', product_url=link))
                    db.commit()
                    return 
                finally:
                    db.close()
        print(f"⚠️ Newegg: No valid results for '{query}'")
    except Exception as e:
        print(f"⚠️ Newegg Error: {e}")