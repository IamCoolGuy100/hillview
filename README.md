# Fourth of July Events Script

This repository contains a simple Python script to fetch and display upcoming
Fourth of July events in **Broomfield, Colorado**.

## Usage

```bash
python3 fourth_of_july_events.py
```

The script fetches event information from a mock API endpoint, filters the data
for events in Broomfield that reference "Fourth of July", determines whether
each event is family-friendly based on keywords in the description, and prints a
chronologically sorted list.

Family-friendly events are marked with the `[FAMILY-FRIENDLY]` tag in the
output.
