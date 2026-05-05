Date: 2026-05-05

What I asked AI to do:
- Help me scaffold mini_project_3_map with the same structure as my other mini projects
- Help me write a working `mbta_helper.py` that geocodes a place name and finds the nearest MBTA stop
- Help me wire two APIs together (Mapbox + MBTA) without committing keys to GitHub
- Help me split the pipeline into clear functions I can test from the terminal
- Help me wrap the helper in a small Flask app with a form, a results page, and a Mapbox map
- Help me handle the obvious failure cases (no place found, no stops nearby, network errors)

What I didn't understand in the generated code:
- Why Mapbox returns coordinates as `[longitude, latitude]` instead of `(lat, lng)`
- How `urllib.parse.quote()` and `urllib.parse.urlencode()` escape spaces and brackets in URLs
- How the MBTA `filter[latitude]` / `filter[longitude]` / `sort=distance` combination actually returns the nearest stop
- What `wheelchair_boarding` values 0, 1, and 2 mean, and why I'm treating 0 (unknown) as not accessible
- How `with urllib.request.urlopen(url) as resp:` works as a context manager
- How `request.method` lets a single Flask route handle both GET and POST
- How `{% extends "base.html" %}` and `{% block content %}` work in Jinja templates
- How the `|tojson` filter safely embeds a Python string inside a JavaScript snippet

What I learned:
- API keys belong in a `.env` file, and `.env` belongs in `.gitignore` — public Mapbox tokens still shouldn't be in the repo
- `urllib.request` + `json` from the standard library is enough — I don't need to install `requests`
- The MBTA V3 API supports `sort=distance` when you give it a lat/lng filter, so the first item in `data` is the nearest stop
- Mapbox nests the result coordinates under `features[0].center` as `[lng, lat]` — easy to flip by accident
- Splitting the pipeline into one function per API call plus a small combiner makes it easy to test each piece in isolation
- Flask's `render_template()` with a base template and `{% block %}` tags is a clean way to share a header/style between pages
- It's fine to handle different errors with different `except` branches and pass a friendly message back into the same template
- For the map, I needed a richer helper (`find_stop_near_details`) that returns coordinates too — I kept the original `find_stop_near` signature so the assignment example (`("Park Street", True)`) still works
- Mapbox GL JS reads `mapboxgl.accessToken` and takes coordinates as `[lng, lat]` (matching the geocoding API but the opposite of how I think about lat/lng)

If I kept working on this project, I would add:
- Friendlier error handling for typos and addresses outside the MBTA service area (suggest "did you mean…")
- A small cache so I don't re-geocode the same place twice
- A second marker color/legend, walking directions, and the distance to the stop
- Filters to find the nearest stop of a specific type (subway only, commuter rail only, etc.)
