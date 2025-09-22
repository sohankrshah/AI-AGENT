import os
import requests
from dotenv import load_dotenv

load_dotenv()

class APIIntegrationService:
    
    def __init__(self):
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        self.exchange_api_key = os.getenv("EXCHANGE_API_KEY")        
        if not self.serpapi_key:
            raise ValueError("SERPAPI_KEY is required for enhanced features")

    def get_exchange_rate(self, from_currency="USD", to_currency="EUR"):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if to_currency in data['rates']:
                return {
                    'rate': data['rates'][to_currency],
                    'date': data['date'],
                    'from': from_currency,
                    'to': to_currency,
                    'success': True
                }
            else:
                raise ValueError(f"Currency {to_currency} not found in exchange rates")
                
        except Exception as e:
            print(f"Exchange rate API error: {e}")
            raise

    def search_flights(self, origin, destination, departure_date, return_date=None, travel_class="economy"):
        try:
            params = {
                "engine": "google_flights",
                "departure_id": origin,
                "arrival_id": destination,
                "outbound_date": departure_date,
                "currency": "USD",
                "travel_class": travel_class,
                "api_key": self.serpapi_key
            }
            
            if return_date:
                params["return_date"] = return_date
            
            response = requests.get("https://serpapi.com/search", params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Flight search API error: {e}")
            raise

    def search_hotels(self, destination, check_in, check_out, adults=2):
        try:
            params = {
                "engine": "google_hotels",
                "q": destination,
                "check_in_date": check_in,
                "check_out_date": check_out,
                "adults": adults,
                "currency": "USD",
                "api_key": self.serpapi_key
            }
            
            response = requests.get("https://serpapi.com/search", params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Hotel search API error: {e}")
            raise

    def get_local_info(self, location, query_type="visa center"):
        try:
            params = {
                "engine": "google",
                "q": f"{query_type} near {location}",
                "location": location,
                "api_key": self.serpapi_key
            }
            
            response = requests.get("https://serpapi.com/search", params=params, timeout=20)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Local search API error: {e}")
            raise

    def get_directions(self, origin, destination, mode="driving"):
        try:
            params = {
                "engine": "google_maps_directions",
                "start_addr": origin,
                "end_addr": destination,
                "travel_mode": mode,
                "api_key": self.serpapi_key
            }
            
            response = requests.get("https://serpapi.com/search", params=params, timeout=20)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Directions API error: {e}")
            raise

    def search_places(self, location, place_type="tourist_attraction"):
        try:
            params = {
                "engine": "google_maps",
                "q": f"{place_type} in {location}",
                "type": "search",
                "api_key": self.serpapi_key
            }
            
            response = requests.get("https://serpapi.com/search", params=params, timeout=20)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Places search API error: {e}")
            raise