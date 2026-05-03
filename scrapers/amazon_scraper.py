import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from database.models import CPU

def scrape_amazon_stealth(url):
    print(f"🕵️  Launching Stealth Browser for Amazon (CAD): {url}")
    
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=147)

    try:
        driver.get(url)
        time.sleep(8) 

        # 1. Clean Title
        raw_title = driver.find_element(By.ID, "productTitle").text.strip()
        clean_title = raw_title.split('-')[0].split(',')[0].split('(')[0].strip()

        # 2. Clean Price
        price_element = driver.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen")
        price_raw = price_element.get_attribute("innerHTML")
        price_cleaned = "".join(char for char in price_raw if char.isdigit() or char == '.')
        price_cad = float(price_cleaned)

        print(f"✅ Found: {clean_title}")
        print(f"💰 Price: ${price_cad} CAD")

        # 3. Save to DB
        db = SessionLocal()
        try:
            new_cpu = CPU(
                brand='AMD',
                model_name=clean_title,
                lowest_price=price_cad,
                currency='CAD',
                product_url=url
            )
            db.add(new_cpu)
            db.commit()
            print("✅ Saved to MySQL!")
        except Exception as e:
            print(f"❌ DB Error: {e}")
            db.rollback()
        finally:
            db.close()

    except Exception as e:
        print(f"❌ Failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_url = "https://www.amazon.com/AMD-Ryzen-7800X3D-16-Thread-Processor/dp/B0BTZB7F88"
    scrape_amazon_stealth(test_url)