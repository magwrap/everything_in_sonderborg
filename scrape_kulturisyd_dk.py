from bs4 import BeautifulSoup
from datetime import datetime
from event import Event
from typing import List


def scrape_kulturisyd_dk(html_content: str, url: str = "") -> List[Event]:
    soup = BeautifulSoup(html_content, 'html.parser')
    event_divs = soup.find_all('div', class_='list-item background')
    events: List[Event] = []

    for event_div in event_divs:
        # Extract name
        name_elem = event_div.find('h2')
        name = name_elem.text.strip() if name_elem else 'No name found'

        # Extract time information
        time_elem = event_div.find('strong')
        time_str = time_elem.text.strip() if time_elem else 'No time found'
        try:
            time = datetime.strptime(time_str, '%d-%m-%Y')
        except ValueError:
            time = None

        # Extract start and end times
        info_div = event_div.find('div', class_='info')
        if info_div:
            time_p = info_div.find('p', recursive=False)
            if time_p:
                time_text = time_p.text.strip()
                time_parts = time_text.split('-')
                start_time = time_parts[0].strip() if len(
                    time_parts) > 0 else None
                end_time = time_parts[1].strip() if len(
                    time_parts) > 1 else None
            else:
                start_time = end_time = None
        else:
            start_time = end_time = None

        # Extract link
        link_elem = event_div.find('a', href=True)
        link = f"{url}{link_elem['href']}" if link_elem else 'No link found'

        # Extract venue
        venue_elem = event_div.find(
            'p', string=lambda text: 'Venue:' in text if text else False)
        venue = venue_elem.text.strip().split(
            'Venue:')[-1].strip() if venue_elem else None

        # Extract description
        description_elem = event_div.find('p', recursive=False)
        description = description_elem.text.strip() if description_elem else None

        # Create Event object
        event = Event(
            name=name,
            time=time,
            link=link,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            description=description
        )
        events.append(event)

    return events
