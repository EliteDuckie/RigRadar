import requests
import undetected_chromedriver as uc
import time

def run_diagnostics():
    print("🕵️‍♂️ --- RIGRADAR DIAGNOSTICS --- 🕵️‍♂️\n")

    # 1. Memory Express Check
    print("📡 Pinging Memory Express...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0"}
    res = requests.get("https://www.memoryexpress.com/Search/Products?Search=Ryzen+7+7800X3D", headers=headers)
    
    print(f"Status Code: {res.status_code}")
    if res.status_code == 403:
        print("❌ FAILED: Memory Express is blocking our Python requests.")
    else:
        card_count = res.text.count("c-shca-icon-item")
        print(f"✅ Success: Page loaded. Found {card_count} product cards in the HTML.")


    # 2. Amazon Vision Check
    print("\n📸 Taking a photo of Amazon...")
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    
    # Using your confirmed Chrome version
    driver = uc.Chrome(options=options, version_main=147)
    
    try:
        driver.get("https://www.amazon.ca/s?k=Ryzen+7+7800X3D")
        time.sleep(6) # Let the page settle
        
        # Take a screenshot of the headless browser
        driver.save_screenshot("amazon_vision.png")
        print("✅ SUCCESS: Saved 'amazon_vision.png' to your folder.")
    except Exception as e:
        print(f"❌ Amazon Vision Failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_diagnostics()