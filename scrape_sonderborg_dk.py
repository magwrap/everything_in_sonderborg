from bs4 import BeautifulSoup
from datetime import datetime
from event import Event
from typing import List


def scrape_sonderborg_dk(html_content: str, url: str = "") -> List[Event]:
    soup = BeautifulSoup(html_content, "html.parser")
    events: List[Event] = []
    event_rows = soup.find_all(
        'div', {'class': 'tribe-events-calendar-list__event-row'})

    for event_row in event_rows:
        # Extract name
        name_elem = event_row.find(
            'h3', {'class': 'tribe-events-calendar-list__event-title'})
        name = name_elem.text.strip() if name_elem else 'No name found'

        # Extract time
        time_elem = event_row.find(
            'time', {'class': 'tribe-events-calendar-list__event-datetime'})
        if time_elem and 'datetime' in time_elem.attrs:
            datetime_str = time_elem['datetime']
            try:
                time = datetime.strptime(datetime_str, '%Y-%m-%d')
            except ValueError:
                time = None
        else:
            time = None

        # Extract start and end times
        start_time_elem = event_row.find(
            'span', {'class': 'tribe-event-date-start'})
        end_time_elem = event_row.find(
            'span', {'class': 'tribe-event-date-end'})
        start_time = start_time_elem.text.strip(
        ) if start_time_elem else 'No start time found'
        end_time = end_time_elem.text.strip() if end_time_elem else 'No end time found'

        # Extract link
        link_elem = event_row.find(
            'a', {'class': 'tribe-events-calendar-list__event-title-link'})
        link = f"{url}{link_elem['href']}" if link_elem else 'No link found'

        # Extract venue (not present in the provided HTML, so leaving it as None)
        venue = None

        # Extract description
        description_elem = event_row.find(
            'div', {'class': 'tribe-events-calendar-list__event-description'})
        description = description_elem.text.strip() if description_elem else None

        # Create Event object
        event = Event(
            name=name,
            time=time,
            start_time=start_time,
            end_time=end_time,
            link=link,
            venue=venue,
            description=description
        )
        events.append(event)

    return events
