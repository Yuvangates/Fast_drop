from fast_drop import settings
import requests

def get_optimized_route(orders):
    """Fetch optimized route including stores and delivery addresses."""
    api_key = settings.GOOGLE_MAPS_API_KEY

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
        return None, None

    origin = addresses[0]  # First store or base
    destination = addresses[-1]  # Last delivery location
    waypoints = '|'.join(addresses[1:-1]) if len(addresses) > 2 else ''

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        polyline = data['routes'][0]['overview_polyline']['points']
        legs = data['routes'][0]['legs']
        return polyline, legs

    return None, None
