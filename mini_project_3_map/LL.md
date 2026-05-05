Date: 2026-05-05

What I asked AI to do:
- Help me scaffold mini_project_3_map with the same structure as my other mini projects
- Help me write a working `mbta_helper.py` that geocodes a place name and finds the nearest MBTA stop
- Help me wire two APIs together (Mapbox + MBTA) without committing keys to GitHub
- Help me split the pipeline into clear functions I can test from the terminal

What I didn't understand in the generated code:
- Why Mapbox returns coordinates as `[longitude, latitude]` instead of `(lat, lng)`
- How `urllib.parse.quote()` and `urllib.parse.urlencode()` escape spaces and brackets in URLs
- How the MBTA `filter[latitude]` / `filter[longitude]` / `sort=distance` combination actually returns the nearest stop
- What `wheelchair_boarding` values 0, 1, and 2 mean, and why I'm treating 0 (unknown) as not accessible
- How `with urllib.request.urlopen(url) as resp:` works as a context manager

What I learned:
- API keys belong in a `.env` file, and `.env` belongs in `.gitignore` — public Mapbox tokens still shouldn't be in the repo
- `urllib.request` + `json` from the standard library is enough — I don't need to install `requests`
- The MBTA V3 API supports `sort=distance` when you give it a lat/lng filter, so the first item in `data` is the nearest stop
- Mapbox nests the result coordinates under `features[0].center` as `[lng, lat]` — easy to flip by accident
- Splitting the pipeline into one function per API call plus a small combiner (`find_stop_near`) makes it easy to test each piece in isolation
- `os.environ.get(...)` returns `None` when a key is missing, which makes for cleaner "is the key set?" checks than wrapping in a try/except

If I kept working on this project, I would add:
- The Flask layer with a form on the home page and a results page
- A Mapbox map on the results page with markers for the input location and the nearest stop
- Friendlier error handling for typos and addresses outside the MBTA service area
- A small cache so I don't re-geocode the same place twice
