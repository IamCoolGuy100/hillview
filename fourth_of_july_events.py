from datetime import datetime
import json
from urllib import request, error

URL = "https://api.npoint.io/4479919fe283e0569927"
CITY = "Broomfield"
STATE = "Colorado"
FAMILY_FRIENDLY_KEYWORDS = ["family-friendly", "all ages", "kids"]


def fetch_events(url: str = URL):
    """Fetch event data from the provided URL."""
    try:
        with request.urlopen(url, timeout=10) as response:
            data = response.read().decode()
    except error.URLError as e:
        print(f"Failed to fetch event data: {e.reason}")
        return []
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        print("Response content is not valid JSON.")
        return []


def is_family_friendly(description: str) -> bool:
    """Determine if the event is family-friendly based on description."""
    if not description:
        return False
    desc = description.lower()
    return any(keyword in desc for keyword in FAMILY_FRIENDLY_KEYWORDS)


def filter_events(events):
    """Filter events for Fourth of July in Broomfield, Colorado."""
    results = []
    for event in events:
        city = event.get("city", "").lower()
        state = event.get("state", "").lower()
        if city != CITY.lower() or state != STATE.lower():
            continue
        name = event.get("name", "")
        if "fourth of july" not in name.lower():
            continue
        start_time = event.get("startTime") or event.get("start_time")
        if not start_time:
            continue
        results.append(
            {
                "name": name,
                "location": event.get("location", ""),
                "startTime": start_time,
                "family_friendly": is_family_friendly(event.get("description", "")),
            }
        )
    return results


def sort_events(events):
    """Sort events chronologically by start time."""
    def parse_time(ev):
        ts = ev.get("startTime")
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except Exception:
            return datetime.max

    return sorted(events, key=parse_time)


def display_events(events):
    """Print formatted event information."""
    if not events:
        print("No upcoming Fourth of July events found.")
        return
    print("Upcoming Fourth of July Events in Broomfield, CO\n")
    for ev in events:
        friendly_tag = "[FAMILY-FRIENDLY]" if ev["family_friendly"] else ""
        print(f"Event: {ev['name']}")
        print(f"Location: {ev['location']}")
        print(f"Start Time: {ev['startTime']}")
        if friendly_tag:
            print(friendly_tag)
        print()


def main():
    events = fetch_events()
    filtered = filter_events(events)
    sorted_events = sort_events(filtered)
    display_events(sorted_events)


if __name__ == "__main__":
    main()
