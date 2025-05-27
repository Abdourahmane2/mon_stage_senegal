from geopy.geocoders import Nominatim

def deviner_region_naissance(lieu_naissance):
    geolocator = Nominatim(user_agent="geoapi_devine_region")

    try:
        location = geolocator.geocode(lieu_naissance + ", Senegal", addressdetails=True, language='fr')
        if location and 'address' in location.raw:
            address = location.raw['address']
            if 'state' in address:
                return address['state'].split()[-1].strip()
            elif 'region' in address:
                return address['region'].split()[-1]
    except Exception as e:
        print(f"Erreur lors du géocodage : {e}")

    return None

# Exemples d'utilisation
print(deviner_region_naissance("MEKHE"))      
print(deviner_region_naissance("YAFERA"))       
print(deviner_region_naissance("Saint-Louis")) 
print(deviner_region_naissance("Ziguinchor"))  
