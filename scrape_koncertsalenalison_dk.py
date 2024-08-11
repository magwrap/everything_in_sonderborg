from bs4 import BeautifulSoup
from datetime import datetime
from event import Event
from typing import List


def scrape_koncertsalenalsion_dk(html_content: str, url: str = "https://koncertsalenalsion.dk") -> List[Event]:
    soup = BeautifulSoup(html_content, 'html.parser')
    event_div = soup.find('div', class_='mod_eventlist block')
    event_blocks = event_div.find_all(
        'div', class_=['event block forside current', 'event block forside upcoming'])
    events: List[Event] = []

    for event_block in event_blocks:
        # Extract name
        name_elem = event_block.find('h2')
        name = name_elem.text.strip() if name_elem else 'No name found'

        # Extract time information
        time_elem = event_block.find('p', class_='info')
        time_str = time_elem.text.strip() if time_elem else 'No time found'
        try:
            time = datetime.strptime(time_str, '%d-%m-%Y')
        except ValueError:
            time = None

        # Extract link
        link_elem = event_block.find('a', href=True)
        link = f"{url}/{link_elem['href']}" if link_elem else 'No link found'

        # Extract description (if available)
        description_elem = event_block.find('div', class_='ce_text')
        description = description_elem.text.strip() if description_elem else None

        # Create Event object
        event = Event(
            name=name,
            time=time,
            link=link,
            start_time=time_str,  # Using the date as start_time
            end_time=None,  # No end time information available
            venue="Koncertsalen Alsion",  # Assuming all events are at this venue
            description=description
        )
        events.append(event)

    return events
