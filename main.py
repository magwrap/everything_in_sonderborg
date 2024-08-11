import requests
from scrape_sonderborg_dk import scrape_sonderborg_dk
from scrape_visit_sonderjylland_dk import scrape_visitsonderjylland_dk
from scrape_kulturisyd_dk import scrape_kulturisyd_dk
from scrape_koncertsalenalison_dk import scrape_koncertsalenalsion_dk
from event import Event
from utils import print_events, print_events_long

SONDERBORG_DK_URL = "https://sonderborg.dk/begivenheder/"
VISITSONDERJYYLAND_DK_URL = "https://www.visitsonderjylland.dk/sonderborg/det-sker/det-sker-i-soenderborg"
KULTURISYD_DK_URL = "https://kulturisyd.dk"
KONCERTSALENALISON_DK_URL = "https://koncertsalenalsion.dk/da/koncertsalen"


def main():
    # Your main program logic goes here
    print("running main")
    all_events: list[Event] = []

    # sonderborg.dk
    print("Downloading the sonderborg.dk data...")
    response = requests.get(SONDERBORG_DK_URL)
    html_content = response.content
    sonderborg_dk_events: list[Event] = scrape_sonderborg_dk(html_content)
    # print_events(sonderborg_dk_events)

    # visitsonderjyyland.dk
    print("Downloading the visitsonderjylland.dk data...")
    response = requests.get(VISITSONDERJYYLAND_DK_URL)
    html_content = response.content
    visitsonderjylland_dk_events: list[Event] = scrape_visitsonderjylland_dk(
        html_content)
    # print_events(visitsonderjylland_dk_events)

    # kulturisyd.dk
    print("Downloading the kulturisyd.dk data...")
    response = requests.get(KULTURISYD_DK_URL)
    html_content = response.content
    kulturisyd_dk_events: list[Event] = scrape_kulturisyd_dk(
        html_content, KULTURISYD_DK_URL)
    # print_events(kulturisyd_dk_events)

    # koncertsalenalsion.dk
    print("Downloading the koncertsalenalsion.dk data...")
    response = requests.get(KONCERTSALENALISON_DK_URL)
    html_content = response.content
    koncertsalenalison_dk_events: list[Event] = scrape_koncertsalenalsion_dk(
        html_content)
    # print_events(koncertsalenalison_dk_events)

    all_events.extend(sonderborg_dk_events)
    all_events.extend(visitsonderjylland_dk_events)
    all_events.extend(kulturisyd_dk_events)
    all_events.extend(koncertsalenalison_dk_events)

    all_events.sort(key=lambda x: x.time)

    print_events_long(all_events)


if __name__ == "__main__":
    main()
