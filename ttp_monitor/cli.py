import argparse
import os
from datetime import date, datetime, timedelta

from dotenv import load_dotenv

from ttp_monitor.worker import Worker

load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ttp_monitor",
        usage="python -m %(prog)s [options]",
        description="Monitor schedule availability for the Trusted Traveler Program",
    )

    parser.add_argument(
        "-d",
        "--date",
        dest="watch_date",
        default=str(date.today()),
        help="Search for availability on a single date",
    )

    parser.add_argument(
        "-l",
        "--loc",
        dest="location",
        type=int,
        default=int(os.environ.get("TTP_DEFAULT_LOCATION", 0)),
        help="Location to search for appointments",
    )

    parser.add_argument(
        "-t",
        "--throttle",
        dest="throttle",
        type=int,
        default=30,
        help="Number of seconds to wait between searches",
    )

    args = parser.parse_args()

    start_date = datetime.strptime(args.watch_date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)

    worker = Worker(location=args.location, start_date=start_date, end_date=end_date)
    worker.run()
