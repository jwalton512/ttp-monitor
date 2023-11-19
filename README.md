# TTP Schedule Monitor

A bot which checks for appointment availability for DHS Trusted Traveler Programs

*Not in any way affiliated with the Department of Homeland Security*

## Installation

Install dependencies with

```
poetry install
```

Copy `.env.example` to `.env` and configure settings as applicable

## Usage
```
usage: poetry run python -m ttp_monitor [options]

Monitor schedule availability for the Trusted Traveler Program

options:
  -h, --help                        show this help message and exit
  -d WATCH_DATE, --date WATCH_DATE  Search for availability on a single date
  -l LOCATION, --loc LOCATION       Location to search for appointments
  -t THROTTLE, --throttle THROTTLE  Number of seconds to wait between searches
```