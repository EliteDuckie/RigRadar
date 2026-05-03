import time
from database.connection import SessionLocal
from database.models import CPU

from scrapers.newegg_scraper import search_newegg_discovery
from scrapers.amazon_scraper import search_amazon
from scrapers.memoryexpress_scraper import search_memoryexpress

def clear_db():
    print("🧹 Clearing old prices from database...")
    db = SessionLocal()
    try:
        db.query(CPU).delete()
        db.commit()
    finally:
        db.close()

def run_rigradar_sync():
    clear_db()
    
    # --- THE ULTIMATE CPU TRACKING LIST ---
    search_queries = [
        # Enthusiast / Heavy Productivity
        "Intel i9 14900K",
        "Ryzen 9 7950X",
        "Ryzen 9 7950X3D",
        
        # High-End / Top-Tier Gaming
        "Intel i7 14700K",
        "Ryzen 7 7800X3D",
        "Ryzen 7 9800X3D", 
        
        # Mid-Range / Best Bang-for-Buck
        "Intel i5 13600K",
        "Intel i5 14600K",
        "Ryzen 5 7600X",
        
        # Budget Kings
        "Ryzen 5 7600",
        "Intel i5 12400F"
    ]
    
    scrapers = [
        search_newegg_discovery, 
        search_amazon, 
        search_memoryexpress
    ]

    print("\n🚀 --- RigRadar Global Sync Initialized ---")
    print(f"Tracking {len(search_queries)} CPUs across 3 Retailers. Estimated time: ~3 mins.")
    
    for query in search_queries:
        print(f"\n📦 TARGET: {query}")
        print("-" * 30)
        for scraper_func in scrapers:
            try:
                scraper_func(query)
                time.sleep(4) # 4-second delay between stores to avoid rate limits
            except Exception as e:
                print(f"⚠️ Error in {scraper_func.__name__}: {e}")
                
        print("⏳ Cooling down before next CPU...")
        time.sleep(6) # 6-second delay between different CPUs
                
    print("\n✅ Sync Complete! Open your Dashboard.")

if __name__ == "__main__":
    run_rigradar_sync()