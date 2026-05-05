Date: 2026-05-05

What I asked AI to do:
- Help me scaffold mini_project_3_map with the same structure as my other mini projects
- Help me write a working `mbta_helper.py` that geocodes a place name and finds the nearest MBTA stop
- Help me wire two APIs together (Mapbox + MBTA) without committing keys to GitHub
- Help me split the pipeline into clear functions I can test from the terminal
- Help me wrap the helper in a small Flask app with a form, a results page, and a Mapbox map
- Help me handle the obvious failure cases (no place found, no stops nearby, network errors)
- Help me strip the visuals back to a minimal, monochrome, light-font feel with dark text only where it matters
- Help me write a real README with setup, run instructions, and screenshots

What I didn't understand in the generated code:
- Why Mapbox returns coordinates as `[longitude, latitude]` instead of `(lat, lng)`
- How `urllib.parse.quote()` and `urllib.parse.urlencode()` escape spaces and brackets in URLs
- How the MBTA `filter[latitude]` / `filter[longitude]` / `sort=distance` combination actually returns the nearest stop
- What `wheelchair_boarding` values 0, 1, and 2 mean, and why I'm treating 0 (unknown) as not accessible
- How `with urllib.request.urlopen(url) as resp:` works as a context manager
- How `request.method` lets a single Flask route handle both GET and POST
- How `{% extends "base.html" %}` and `{% block content %}` work in Jinja templates
- What the haversine formula is actually doing — converting lat/lng pairs into a great-circle distance in meters

What I learned:
- API keys belong in a `.env` file, and `.env` belongs in `.gitignore` — public Mapbox tokens still shouldn't be in the repo
- `urllib.request` + `json` from the standard library is enough — I don't need to install `requests`
- The MBTA V3 API supports `sort=distance` when you give it a lat/lng filter, so the first item in `data` is the nearest stop
- Mapbox nests the result coordinates under `features[0].center` as `[lng, lat]` — easy to flip by accident
- Splitting the pipeline into one function per API call plus a small combiner makes it easy to test each piece in isolation
- It's fine to keep two helper signatures side by side: the simple one (`find_stop_near`) the assignment asked for, and a richer one (`find_stop_near_details`) for the Flask map — neither side has to carry the other's complexity
- Flask's `render_template()` with a base template and `{% block %}` tags is a clean way to share styling between pages
- Catching different errors with different `except` branches and passing a friendly message back into the same template is enough — I don't need a separate error page
- A "real" feel doesn't mean adding more chrome. Stripping the page to monochrome with light font weights and dark text only on the answer (the stop name, the yes/no, the distance) feels more finished than a colored card-heavy layout
- Mapbox's `light-v11` style + same-colored `#111` markers makes the map blend with the page instead of fighting it
- A useful README is mostly: what it does, how to set up, how to run, and what the project structure is — anything else is bonus

If I kept working on this project, I would add:
- Friendlier error handling for typos (suggest "did you mean…")
- A small cache so I don't re-geocode the same place twice
- Walking directions and the actual route between the two markers
- Filters to find the nearest stop of a specific type (subway only, commuter rail only, etc.)
- A keyboard-only quick-search experience without leaving the home page
