import undetected_chromedriver as uc
import time

def debug_amazon_view(query):
    url = f"https://www.amazon.ca/s?k={query}"
    options = uc.ChromeOptions()
    # options.add_argument('--headless') # Keep it visible for debugging
    driver = uc.Chrome(options=options, version_main=147)
    
    try:
        driver.get(url)
        time.sleep(10) # Give it plenty of time
        with open("amazon_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📸 Captured Amazon! Open 'amazon_debug.html' in your browser.")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_amazon_view("7800X3D")