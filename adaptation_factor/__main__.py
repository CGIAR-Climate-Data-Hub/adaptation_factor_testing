"""Command-line interface."""

import argparse
import json

from .model import StressBand
from .store import AdaptationStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Store and aggregate E-stress evidence")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "list"):
        command = commands.add_parser(name)
        command.add_argument("database")
    load = commands.add_parser("import-csv")
    load.add_argument("database")
    load.add_argument("csv")
    aggregate = commands.add_parser("aggregate")
    aggregate.add_argument("database")
    aggregate.add_argument("--outcome-unit", required=True)
    aggregate.add_argument("--stress-band", choices=[band.value for band in StressBand])
    args = parser.parse_args()
    store = AdaptationStore(args.database)
    if args.command == "init":
        store.initialize()
        print(f"Initialized {args.database}")
    elif args.command == "import-csv":
        print(f"Imported {store.import_csv(args.csv)} estimate(s)")
    elif args.command == "list":
        print(json.dumps([dict(row) for row in store.rows()], indent=2))
    else:
        band = StressBand(args.stress_band) if args.stress_band else None
        print(json.dumps(store.aggregate(args.outcome_unit, band), indent=2))


if __name__ == "__main__":
    main()

