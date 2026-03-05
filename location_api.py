import requests

def get_location_by_ip() -> dict | None:
    """
    Uses ip-api.com (Free for non-commercial use) to estimate city + coordinates.
    High reliability, no API key required.
    """
    try:
        # Using ip-api.com which is very reliable for free tier
        response = requests.get("http://ip-api.com/json/", timeout=8)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            return {
                "city": data.get("city"),
                "lat": float(data.get("lat")),
                "lon": float(data.get("lon")),
                "country": data.get("country"),
                "region": data.get("regionName"),
            }
        
        # Fallback to ipapi.co if the first one fails
        response = requests.get("https://ipapi.co/json/", timeout=8)
        data = response.json()
        if data.get("city"):
            return {
                "city": data.get("city"),
                "lat": float(data.get("latitude")),
                "lon": float(data.get("longitude")),
                "country": data.get("country_name"),
                "region": data.get("region"),
            }
            
        return None
    except Exception:
        return None
