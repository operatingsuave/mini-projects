# Nearest MBTA Stop

A small Flask web app that finds the closest MBTA stop to any place name or address in the Boston area.

## What It Does

You type a place name. The app:

1. Sends it to the Mapbox Geocoding API to get latitude/longitude
2. Sends those coordinates to the MBTA V3 API to find the nearest stop (sorted by distance)
3. Shows the stop name, wheelchair accessibility, distance away, and a map with both points

## How It Works

The pipeline lives in `mbta_helper.py` as plain Python functions you can run from the terminal without Flask:

- `get_lat_lng(place_name)` → `(lat, lng)` from Mapbox
- `get_nearest_station(lat, lng)` → `(stop_name, accessible)` from MBTA
- `find_stop_near(place_name)` → combines both, e.g. `("Park Street", True)`
- `find_stop_near_details(place_name)` → richer dict with both sets of coordinates and the distance, used by the Flask map

`app.py` is a thin Flask layer on top: a single `/` route handles GET (form) and POST (lookup) and renders one of two templates.

## Setup

You'll need:

- Python 3.9+
- A Mapbox public token — sign up at [mapbox.com](https://mapbox.com) and copy the default `pk.…` token
- (Optional) An MBTA API key — request one at [api-v3.mbta.com](https://api-v3.mbta.com); the app works without one but is rate-limited

From inside the `mini_project_3_map` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# open .env and paste your real MAPBOX_TOKEN (and MBTA_API_KEY if you have one)
```

`.env` is gitignored so the keys never get committed.

## How to Run

Web app:

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Or just the helper, from the terminal:

```bash
python mbta_helper.py "Boston Common"
```

```
--- MBTA Helper ---

Looking up nearest MBTA stop to: Boston Common

  Nearest stop:          Park Street
  Wheelchair accessible: yes
```

## Screenshots

Home page (search form):

![Home page](screenshots/home.png)

Result page (stop, accessibility, distance, map):

![Result page](screenshots/result.png)

## Project Structure

```
mini_project_3_map/
├── app.py              # Flask app (one route, GET + POST)
├── mbta_helper.py      # API pipeline; runnable on its own
├── requirements.txt    # Flask
├── templates/
│   ├── base.html       # shared layout + minimal CSS
│   ├── index.html      # search form
│   └── result.html     # stop info + Mapbox map
├── screenshots/
├── .env.example
├── .gitignore
├── PROPOSAL.md
└── LL.md
```

## Errors I Handle

- **Empty input** → form re-renders with "Please enter a place name."
- **Place not found** → Mapbox returns no features, app shows "No location found for '…'"
- **No nearby stops** → MBTA returns an empty list, app shows "No MBTA stops found near (…, …)"
- **API unreachable** → network error caught and shown as a friendly message instead of a stack trace
- **Missing token** → server-side config error surfaced clearly so you know to fix `.env`

## Tech Notes

- Standard library only for the API calls (`urllib.request`, `json`) — no `requests` dependency
- Tiny inline `.env` reader so I don't depend on `python-dotenv`
- Custom CSS, no Bootstrap — monochrome, light fonts, dark for the values that matter
- Mapbox `light-v11` style and matching `#111` markers to keep the map quiet
- Distance calculated with the haversine formula in `mbta_helper.haversine_meters()`

## Two-Pass Reflection

The first pass got the API pipeline working in the terminal — `find_stop_near("Boston Common")` returning `("Park Street", True)`. That kept the data flow honest: Mapbox returns `[lng, lat]` (not lat/lng), and the MBTA API needs `sort=distance` for the first item to actually be the nearest.

The second pass was the Flask wrapper. The interesting part was deciding how much to share between the helper and the app: I kept the simple `find_stop_near()` from the assignment intact and added a richer `find_stop_near_details()` for the map view, so neither side carries the other's complexity.

The third pass was visual. Started with a card-and-accent-color look, then stripped it back to monochrome with light fonts and dark text only on the things that matter (the stop name, the yes/no, the distance). Less interface, more answer.
