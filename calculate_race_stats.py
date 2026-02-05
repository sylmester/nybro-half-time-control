#!/usr/bin/env python3
"""
Race Stats Calculator

Reads a lap_times CSV in the format:
  timestamp,race_number,hallway,gender,lap1,lap2,...,finish_time
and outputs fun stats:
- Total distance recorded by each hallway
- Total distance by gender
- Fastest lap by gender
- Top 10 finish times per gender

Usage:
    python3 calculate_race_stats.py --csv path/to/lap_times_*.csv --lap-length 2.5 --out stats.txt

If --csv is omitted, the script will use the latest lap_times_*.csv in the current directory.
If --out is omitted, it writes stats_<timestamp>.txt in the current directory and also prints to stdout.
"""

import argparse
import csv
import glob
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate race stats from lap_times CSV")
    parser.add_argument("--csv", dest="csv_path", default=None, help="Path to lap_times CSV (default: latest lap_times_*.csv)")
    parser.add_argument("--lap-length", dest="lap_length", type=float, default=2.5, help="Lap length in km (default: 2.5)")
    parser.add_argument("--out", dest="out_path", default=None, help="Output stats file path (default: stats_<timestamp>.txt)")
    return parser.parse_args()


def latest_lap_times_csv() -> Optional[str]:
    candidates = glob.glob("lap_times_*.csv")
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


def parse_elapsed(s: str) -> Optional[timedelta]:
    """Parse 'HH:MM:SS.mmm' to timedelta. Returns None if blank/invalid."""
    if not s:
        return None
    s = s.strip()
    if not s:
        return None
    try:
        # Expect HH:MM:SS.mmm
        hh, mm, rest = s.split(":")
        ss, ms = rest.split(".")
        return timedelta(hours=int(hh), minutes=int(mm), seconds=int(ss), milliseconds=int(ms))
    except Exception:
        return None


def format_td(td: timedelta) -> str:
    total_ms = int(td.total_seconds() * 1000)
    hours = total_ms // (3600 * 1000)
    minutes = (total_ms // (60 * 1000)) % 60
    seconds = (total_ms // 1000) % 60
    ms = total_ms % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02}.{ms:03}"


def load_rows(csv_path: str) -> Tuple[List[Dict[str, str]], List[str]]:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        # Identify lap columns ordered numerically
        lap_cols = [c for c in reader.fieldnames if c.startswith("lap")]
        lap_cols.sort(key=lambda x: int(x.replace("lap", "")))
        return rows, lap_cols


def compute_stats(rows: List[Dict[str, str]], lap_cols: List[str], lap_length_km: float):
    by_hallway_distance: Dict[str, float] = {}
    by_gender_distance: Dict[str, float] = {}
    fastest_lap_by_gender: Dict[str, Tuple[timedelta, str, str, int]] = {}  # gender -> (split_time, race_number, hallway, lap_index)
    finish_times_by_gender: Dict[str, List[Tuple[timedelta, str, str]]] = {}

    for row in rows:
        hallway = (row.get("hallway") or "").strip() or "Unknown"
        gender = (row.get("gender") or "").strip() or "Unknown"
        race_number = (row.get("race_number") or "").strip() or "?"

        # Parse laps for this runner
        laps_td: List[timedelta] = []
        for i, lap_col in enumerate(lap_cols, start=1):
            td = parse_elapsed(row.get(lap_col, ""))
            if td is not None:
                laps_td.append(td)

        # Compute per-lap splits and track fastest split by gender
        prev = timedelta(0)
        for i, td in enumerate(laps_td, start=1):
            split = td - prev
            prev = td
            current = fastest_lap_by_gender.get(gender)
            if current is None or split < current[0]:
                fastest_lap_by_gender[gender] = (split, race_number, hallway, i)

        lap_count = len(laps_td)
        distance = lap_count * lap_length_km
        by_hallway_distance[hallway] = by_hallway_distance.get(hallway, 0.0) + distance
        by_gender_distance[gender] = by_gender_distance.get(gender, 0.0) + distance

        # Finish time
        finish_td = parse_elapsed(row.get("finish_time", ""))
        if finish_td is not None:
            finish_times_by_gender.setdefault(gender, []).append((finish_td, race_number, hallway))

    # Sort top 10 finish per gender
    top10_finish_by_gender: Dict[str, List[Tuple[timedelta, str, str]]] = {}
    for g, items in finish_times_by_gender.items():
        items.sort(key=lambda x: x[0])
        top10_finish_by_gender[g] = items[:10]

    return {
        "by_hallway_distance": by_hallway_distance,
        "by_gender_distance": by_gender_distance,
        "fastest_lap_by_gender": fastest_lap_by_gender,
        "top10_finish_by_gender": top10_finish_by_gender,
    }


def write_stats_text(out_path: str, stats, lap_length_km: float, csv_path: str):
    lines: List[str] = []
    lines.append("=" * 72)
    lines.append("Race Stats Summary")
    lines.append("=" * 72)
    lines.append(f"Source CSV: {csv_path}")
    lines.append(f"Lap length: {lap_length_km:.3f} km")
    lines.append("")

    lines.append("Total Distance by Hallway (km):")
    for hallway, dist in sorted(stats["by_hallway_distance"].items(), key=lambda x: x[0]):
        lines.append(f"- {hallway}: {dist:.2f} km")
    lines.append("")

    lines.append("Total Distance by Gender (km):")
    for gender, dist in sorted(stats["by_gender_distance"].items(), key=lambda x: x[0]):
        lines.append(f"- {gender}: {dist:.2f} km")
    lines.append("")

    lines.append("Fastest Lap (Split) by Gender:")
    fastest = stats["fastest_lap_by_gender"]
    if fastest:
        for gender, (td, race_number, hallway, lap_index) in sorted(fastest.items(), key=lambda x: x[0]):
            lines.append(f"- {gender}: {format_td(td)} (Runner #{race_number}, {hallway}, lap {lap_index})")
    else:
        lines.append("- No laps recorded")
    lines.append("")

    lines.append("Top 10 Finish Times by Gender:")
    top10 = stats["top10_finish_by_gender"]
    if top10:
        for gender, items in sorted(top10.items(), key=lambda x: x[0]):
            lines.append(f"- {gender}:")
            if items:
                for idx, (td, race_number, hallway) in enumerate(items, start=1):
                    lines.append(f"  {idx:2}. {format_td(td)} (Runner #{race_number}, {hallway})")
            else:
                lines.append("  No finishers")
    else:
        lines.append("- No finishers recorded")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # Also print to stdout for convenience
    print("\n".join(lines))
    print(f"\n✓ Wrote stats: {out_path}")


def main():
    args = parse_args()
    csv_path = args.csv_path or latest_lap_times_csv()
    if not csv_path or not os.path.exists(csv_path):
        raise SystemExit("No lap_times CSV found. Provide --csv or place lap_times_*.csv in current directory.")

    rows, lap_cols = load_rows(csv_path)
    stats = compute_stats(rows, lap_cols, args.lap_length)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = args.out_path or f"stats_{timestamp}.txt"

    write_stats_text(out_path, stats, args.lap_length, csv_path)


if __name__ == "__main__":
    main()
