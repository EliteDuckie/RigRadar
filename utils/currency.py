import requests

def get_usd_to_cad_rate():
    try:
        # Using a free, no-key-required API (ExchangeRate-API)
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        return data['rates']['CAD']
    except Exception as e:
        print(f"⚠️ Could not fetch live rate, using fallback: {e}")
        return 1.37 # Fallback estimate