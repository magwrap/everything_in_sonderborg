from event import Event


def print_events(events: list[Event]) -> None:
    # Print the scraped data if requested
    for event in events:
        print(event)
        print(f"Venue: {event.venue}")
        print(f"Link: {event.link}")
        print("---")


def print_events_long(events: list[Event]) -> None:
    for event in events:
        print(f"Name: {event.name}")
        print(f"Time: {event.time}")
        print(f"Link: {event.link}")
        print(f"Start Time: {event.start_time}")
        print(f"End Time: {event.end_time}")
        print(f"Venue: {event.venue}")
        print(f"Description: {event.description}")
        print()
