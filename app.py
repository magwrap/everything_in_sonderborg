from flask import Flask, render_template
from scraping.scrape_sonderborg_dk import scrape_sonderborg_dk
from scraping.scrape_visit_sonderjylland_dk import scrape_visitsonderjylland_dk
from scraping.scrape_kulturisyd_dk import scrape_kulturisyd_dk
from scraping.scrape_koncertsalenalison_dk import scrape_koncertsalenalsion_dk
from datetime import datetime
from event import Event
import requests

SONDERBORG_DK_URL = "https://sonderborg.dk/begivenheder/"
VISITSONDERJYYLAND_DK_URL = "https://www.visitsonderjylland.dk/sonderborg/det-sker/det-sker-i-soenderborg"
KULTURISYD_DK_URL = "https://kulturisyd.dk"
KONCERTSALENALISON_DK_URL = "https://koncertsalenalsion.dk/da/koncertsalen"

app = Flask(__name__)


@app.route('/')
def index():
    all_events: list[Event] = []

    # sonderborg.dk
    print("Downloading the sonderborg.dk data...")
    response = requests.get(SONDERBORG_DK_URL)
    html_content = response.content
    sonderborg_dk_events: list[Event] = scrape_sonderborg_dk(html_content)
    # visitsonderjyyland.dk
    print("Downloading the visitsonderjylland.dk data...")
    response = requests.get(VISITSONDERJYYLAND_DK_URL)
    html_content = response.content
    visitsonderjylland_dk_events: list[Event] = scrape_visitsonderjylland_dk(
        html_content)

    # kulturisyd.dk
    print("Downloading the kulturisyd.dk data...")
    response = requests.get(KULTURISYD_DK_URL)
    html_content = response.content
    kulturisyd_dk_events: list[Event] = scrape_kulturisyd_dk(
        html_content, KULTURISYD_DK_URL)

    # koncertsalenalsion.dk
    print("Downloading the koncertsalenalsion.dk data...")
    response = requests.get(KONCERTSALENALISON_DK_URL)
    html_content = response.content
    koncertsalenalison_dk_events: list[Event] = scrape_koncertsalenalsion_dk(
        html_content)

    # Combine all the events into a single list
    all_events.extend(sonderborg_dk_events)
    all_events.extend(visitsonderjylland_dk_events)
    all_events.extend(kulturisyd_dk_events)
    all_events.extend(koncertsalenalison_dk_events)

    # Sort the events based on the event time
    all_events.sort(key=lambda x: x.time)

    # Remove events that have already happened
    current_date = datetime.now().date()
    all_events = [event for event in all_events if event.time.date()
                  >= current_date]

    return render_template('index.html', events=all_events)


if __name__ == '__main__':
    app.run(debug=True)
