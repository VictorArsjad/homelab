#!/usr/bin/env python3
import csv
import sys
from datetime import datetime
from pathlib import Path


def parse_rate(value: str) -> str | None:
    cleaned = value.strip().replace(",", "")
    return cleaned if cleaned else None


def parse_timestamp(value: str) -> str:
    return datetime.strptime(value.strip(), "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S+00")


def csv_to_sql(csv_path: Path, output_path: Path) -> None:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        currencies = [col for col in reader.fieldnames if col != "Time"]
        col_names = [c.lower() for c in currencies]

        rows = []
        for row in reader:
            ts = parse_timestamp(row["Time"])
            rate_values = ", ".join(parse_rate(row[c]) or "NULL" for c in currencies)
            rows.append(f"('{ts}', {rate_values}, 'migration')")

    columns = "ts_utc, " + ", ".join(col_names) + ", source"
    with output_path.open("w", encoding="utf-8") as f:
        f.write(f"INSERT INTO fx_rates ({columns})\nVALUES\n")
        f.write(",\n".join(f"  {r}" for r in rows))
        f.write(";\n")

    print(f"Written {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.csv> [output.sql]")
        sys.exit(1)

    csv_file = Path(sys.argv[1])
    sql_file = Path(sys.argv[2]) if len(sys.argv) > 2 else csv_file.with_suffix(".sql")
    csv_to_sql(csv_file, sql_file)
