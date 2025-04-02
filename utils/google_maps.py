from fast_drop import settings
import requests
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)

def get_optimized_route(orders):
    """Fetch optimized route including stores and delivery addresses."""
    api_key = settings.GOOGLE_MAPS_API_KEY

    try:
        addresses = set()

        for order in orders:
            # Add the store address directly from the order's store
            if order.store and order.store.address:
                addresses.add(order.store.address)  # Directly using store's address
            
            # Add delivery address of the order
            delivery_address = f"{order.address}, {order.city}, {order.state}, {order.pincode}"
            addresses.add(delivery_address)

        addresses = list(addresses)  # Convert set to list to maintain order

        if not addresses:
            logger.warning("No addresses found for route optimization")
            return None, None

        origin = addresses[0]  # First store or base
        destination = addresses[-1]  # Last delivery location
        waypoints = '|'.join(addresses[1:-1]) if len(addresses) > 2 else ''

        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={api_key}"

        # Add timeout and retry settings
        response = requests.get(url, timeout=10, verify=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if data['status'] == 'OK':
            polyline = data['routes'][0]['overview_polyline']['points']
            legs = data['routes'][0]['legs']
            return polyline, legs
        else:
            logger.error(f"Google Maps API returned status: {data['status']}")
            return None, None

    except requests.exceptions.Timeout:
        logger.error("Timeout while connecting to Google Maps API")
        return None, None
    except requests.exceptions.ConnectionError:
        logger.error("Connection error while connecting to Google Maps API")
        return None, None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while connecting to Google Maps API: {str(e)}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error in get_optimized_route: {str(e)}")
        return None, None
