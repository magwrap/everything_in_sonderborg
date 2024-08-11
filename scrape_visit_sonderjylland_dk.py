from bs4 import BeautifulSoup
from datetime import datetime
from event import Event
from typing import List

# WARNING: not working


def scrape_visitsonderjylland_dk(html_content: str, url: str = "https://www.visitsonderjylland.dk/sonderborg/det-sker/det-sker-i-soenderborg") -> List[Event]:
    soup = BeautifulSoup(html_content, 'html.parser')
    event_div = soup.find('div', id='nautcontent')
    if event_div:
        event_blocks = event_div.find_all(
            'div', class_='no1 nautevent Col__Wrap-sc-6ejptb-0 giEjcR xs-12 md-4')
        events: List[Event] = []

        for event_block in event_blocks:
            # Extract name
            name_elem = event_block.find(
                'h3', class_='ProductPreview__Title-sc-1amn7ly-4 eketke')
            name = name_elem.text.strip() if name_elem else 'No name found'

            # Extract time information
            time_elem = event_block.find('div', class_='eventdate notranslate')
            time_str = time_elem.text.strip() if time_elem else 'No time found'
            try:
                time = datetime.strptime(time_str, '%d.%m.%Y')
            except ValueError:
                time = None

            # Extract link
            link_elem = event_block.find('a', href=True)
            link = link_elem['href'] if link_elem else 'No link found'

            # Extract description (if available)
            description_elem = event_block.find('p')
            description = description_elem.text.strip() if description_elem else None

            # Create Event object
            event = Event(
                name=name,
                time=time,
                link=link,
                start_time=time_str,  # Using the date as start_time
                end_time=None,  # No end time information available
                venue="Sønderborg",  # Assuming all events are in Sønderborg
                description=description
            )
            events.append(event)

        return events
    else:
        return []
