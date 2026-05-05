"""mbta_helper.py — find the nearest MBTA stop to a place name.

Pipeline:  place name  ->  Mapbox geocoding  ->  (lat, lng)  ->  MBTA V3 API  ->  nearest stop.

Run from the terminal:
    python mbta_helper.py "Boston Common"
"""

import json
import os
import sys
import urllib.parse
import urllib.request


MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


def load_env(path=".env"):
    """Tiny .env reader so we don't need python-dotenv. Reads KEY=VALUE lines into os.environ."""
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), value)


def http_get_json(url):
    """GET a URL and return the decoded JSON body."""
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_lat_lng(place_name):
    """Use the Mapbox Geocoding API to convert a place name into (latitude, longitude)."""
    token = os.environ.get("MAPBOX_TOKEN")
    if not token:
        raise RuntimeError("MAPBOX_TOKEN is not set. Add it to your .env file.")

    query = urllib.parse.quote(place_name)
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={token}&limit=1"
    data = http_get_json(url)

    features = data.get("features") or []
    if not features:
        raise ValueError(f"No location found for '{place_name}'")

    # Mapbox returns coordinates as [longitude, latitude] — flip them.
    lng, lat = features[0]["center"]
    return lat, lng


def _fetch_nearest_stop(lat, lng):
    """Internal helper: query MBTA V3 and return the raw attributes dict for the nearest stop."""
    params = {
        "filter[latitude]": lat,
        "filter[longitude]": lng,
        "sort": "distance",
        "page[limit]": 1,
    }
    api_key = os.environ.get("MBTA_API_KEY")
    if api_key:
        params["api_key"] = api_key

    url = f"{MBTA_BASE_URL}?{urllib.parse.urlencode(params)}"
    data = http_get_json(url)

    stops = data.get("data") or []
    if not stops:
        raise ValueError(f"No MBTA stops found near ({lat}, {lng})")

    return stops[0]["attributes"]


def get_nearest_station(lat, lng):
    """Use the MBTA V3 API to find the nearest stop. Returns (stop_name, wheelchair_accessible)."""
    attrs = _fetch_nearest_stop(lat, lng)
    name = attrs.get("name", "Unknown stop")
    # wheelchair_boarding: 0 = no info, 1 = accessible, 2 = not accessible
    accessible = attrs.get("wheelchair_boarding") == 1
    return name, accessible


def find_stop_near(place_name):
    """End-to-end: place name -> nearest MBTA stop. Returns (stop_name, wheelchair_accessible)."""
    lat, lng = get_lat_lng(place_name)
    return get_nearest_station(lat, lng)


def find_stop_near_details(place_name):
    """Like find_stop_near but returns a dict with both sets of coordinates — for the Flask map."""
    place_lat, place_lng = get_lat_lng(place_name)
    attrs = _fetch_nearest_stop(place_lat, place_lng)
    return {
        "stop": attrs.get("name", "Unknown stop"),
        "accessible": attrs.get("wheelchair_boarding") == 1,
        "place_lat": place_lat,
        "place_lng": place_lng,
        "stop_lat": attrs.get("latitude"),
        "stop_lng": attrs.get("longitude"),
    }


def main():
    load_env()

    if len(sys.argv) < 2:
        place = "Boston Common"
    else:
        place = " ".join(sys.argv[1:])

    print(f"\n--- MBTA Helper ---")
    print(f"\nLooking up nearest MBTA stop to: {place}")

    try:
        stop, accessible = find_stop_near(place)
    except Exception as e:
        print(f"\n  Error: {e}\n")
        sys.exit(1)

    print(f"\n  Nearest stop:          {stop}")
    print(f"  Wheelchair accessible: {'yes' if accessible else 'no'}\n")


if __name__ == "__main__":
    main()
