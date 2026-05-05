## Project Proposal

**What I'm building:**
I'm building a Flask web app that helps people find the nearest MBTA station. The user enters a place name or address, the app geocodes it using the Mapbox API, queries the MBTA V3 API for the closest stop, and shows the result on a page — ideally on a map.

**Why I chose this:**
One of the suggested projects. It ties two real APIs together and ends as something I can actually open in a browser, not just a terminal script.

**Core features:**
- A homepage with a form to enter a place name or address
- A Mapbox geocoding call that turns the place name into latitude/longitude
- An MBTA V3 API call that finds the nearest stop to those coordinates
- A results page that shows the stop name and whether it's wheelchair accessible
- A map view of the input location and the nearest stop (stretch)

**What I don't know yet:**
- The exact request format for the MBTA `/stops` endpoint and how to sort by distance
- The cleanest way to keep the Mapbox token and MBTA API key out of the repo
- How Flask templates and forms wire up to routes
- How to drop a Mapbox map into a results page without overcomplicating it
