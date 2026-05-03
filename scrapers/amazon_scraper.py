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

def search_amazon(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.amazon.ca/s?k={encoded_query}"
    print(f"🔎 Amazon Search: {query}")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless') 
    driver = uc.Chrome(options=options, version_main=147) 
    
    try:
        driver.get(url)
        time.sleep(7)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # BULLETPROOF: Extract the raw model number and strip all symbols (e.g. "7800X3D")
        pure_model = re.sub(r'[^a-z0-9]', '', query.split()[-1].lower())
        
        # --- SCENARIO A: Redirected directly to product page ---
        pdp_title = soup.find(id='productTitle')
        if pdp_title:
            name = pdp_title.text.strip()
            pure_name = re.sub(r'[^a-z0-9]', '', name.lower())
            
            # Guardrails for Direct Pages
            if pure_model in pure_name and not ("x3d" not in pure_model and "x3d" in pure_name):
                price_span = soup.find('span', class_='a-price-whole')
                if price_span:
                    price_text = price_span.text.replace(',', '').replace('.', '').strip()
                    fraction = soup.find('span', class_='a-price-fraction')
                    cents = fraction.text.strip() if fraction else "00"
                    try:
                        final_price = float(f"{price_text}.{cents}")
                        print(f"✅ Amazon Match (Direct): {name[:35]}... @ ${final_price}")
                        db = SessionLocal()
                        db.add(CPU(brand="AMD" if "AMD" in name.upper() else "Intel",
                                   model_name=name[:100], lowest_price=final_price,
                                   currency='CAD', product_url=driver.current_url))
                        db.commit()
                        db.close()
                        return
                    except ValueError:
                        pass

        # --- SCENARIO B: Search Grid/List Page ---
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for result in results:
            title_tag = result.find(class_=lambda x: x and 'a-text-normal' in x)
            if not title_tag: continue
            
            name = title_tag.text.strip()
            pure_name = re.sub(r'[^a-z0-9]', '', name.lower())
            
            # --- STRICT MATCH GUARDRAILS ---
            if pure_model not in pure_name:
                continue # Amazon showed us a 9950X instead of 7950X
            if "x3d" not in pure_model and "x3d" in pure_name:
                continue # Amazon showed us an X3D
                
            price_span = result.find('span', class_='a-price-whole')
            if not price_span: continue
            
            a_tag = title_tag.find_parent('a')
            if not a_tag:
                a_tag = result.find('a', class_='a-link-normal')
            if not a_tag or 'href' not in a_tag.attrs: continue
            
            link = "https://www.amazon.ca" + a_tag['href']
            price_text = price_span.text.replace(',', '').replace('.', '').strip()
            fraction = result.find('span', class_='a-price-fraction')
            cents = fraction.text.strip() if fraction else "00"
            
            try:
                final_price = float(f"{price_text}.{cents}")
                print(f"✅ Amazon Match: {name[:35]}... @ ${final_price}")
                db = SessionLocal()
                db.add(CPU(brand="AMD" if "AMD" in name.upper() else "Intel",
                           model_name=name[:100], lowest_price=final_price,
                           currency='CAD', product_url=link))
                db.commit()
                db.close()
                return 
            except ValueError:
                continue

        print(f"⚠️ Amazon: No exact match found for '{query}'")
    except Exception as e:
        print(f"❌ Amazon Error: {e}")
    finally:
        driver.quit()