"""Flask web app: nearest MBTA stop finder.

Run from the terminal:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os
import urllib.error

from flask import Flask, render_template, request

import mbta_helper


mbta_helper.load_env()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    place = (request.form.get("place") or "").strip()
    if not place:
        return render_template("index.html", error="Please enter a place name.")

    try:
        result = mbta_helper.find_stop_near_details(place)
    except ValueError as e:
        # Place not found, or no MBTA stops nearby.
        return render_template("index.html", error=str(e), place=place)
    except RuntimeError as e:
        # Missing API token in server env.
        return render_template("index.html", error=f"Server is misconfigured: {e}")
    except urllib.error.URLError:
        return render_template(
            "index.html",
            error="Couldn't reach the Mapbox or MBTA API. Check your connection and try again.",
            place=place,
        )

    return render_template(
        "result.html",
        place=place,
        result=result,
        mapbox_token=os.environ.get("MAPBOX_TOKEN", ""),
    )


if __name__ == "__main__":
    app.run(debug=True)
