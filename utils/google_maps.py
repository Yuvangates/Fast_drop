def get_optimized_route(orders):
    """Fetch optimized route including stores and delivery addresses."""
    api_key = settings.GOOGLE_MAPS_API_KEY

    addresses = []
    store_addresses = set()

    for order in orders:
        # Add store address based on ordered items' store
        for item in order.items.all():
            store = item.item.store
            store_address = f"{store.address}, {store.city}, {store.state}, {store.pincode}"
            
            if store_address not in store_addresses:
                store_addresses.add(store_address)
                addresses.append(store_address)
        
        # Add delivery address of the order
        delivery_address = f"{order.address}, {order.city}, {order.state}, {order.pincode}"
        addresses.append(delivery_address)

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
