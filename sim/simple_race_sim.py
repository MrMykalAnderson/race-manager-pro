"""
Simple Race Simulator for Race Manager Pro

- Loads race session data from a JSON file (track, cars, drivers, entries)
- Simulates a race session (lap times, positions)
- Outputs session results as a JSON structure
"""
import json
import random
from pathlib import Path

INPUT_FILE = Path(__file__).parent.parent / "docs" / "dev" / "SAMPLE_4_CAR_RACE.json"

# Simulation parameters
BASE_LAP_TIME = 60.0  # seconds (for a 2km oval)
LAP_TIME_VARIANCE = 0.5  # seconds, random lap-to-lap variation
SKILL_FACTOR = 2.0  # seconds, max lap time difference due to skill


def load_race_data(path):
    with open(path, "r") as f:
        return json.load(f)


def simulate_race(session_data):
    track = session_data["track"]
    laps = track["laps"]
    entries = session_data["entries"]
    cars = {c["car_id"]: c for c in session_data["cars"]}
    drivers = {d["driver_id"]: d for d in session_data["drivers"]}

    # Build entry list with driver/car info
    entry_list = []
    for entry in entries:
        car = cars[entry["car_id"]]
        driver = drivers[entry["driver_id"]]
        entry_list.append({
            "entry_id": entry["entry_id"],
            "car": car,
            "driver": driver,
            "laps": [],
            "total_time": 0.0
        })

    # Simulate each lap
    for lap_num in range(1, laps + 1):
        for entry in entry_list:
            base = BASE_LAP_TIME
            # Skill reduces lap time
            skill_adj = (1.0 - entry["driver"]["skill"]) * SKILL_FACTOR
            lap_time = base + skill_adj + random.uniform(-LAP_TIME_VARIANCE, LAP_TIME_VARIANCE)
            entry["laps"].append({"lap": lap_num, "lap_time": lap_time})
            entry["total_time"] += lap_time

    # Sort by total time (lowest = winner)
    entry_list.sort(key=lambda e: e["total_time"])
    # Assign positions
    for pos, entry in enumerate(entry_list, 1):
        entry["position"] = pos

    # Build results
    results = {
        "track": track,
        "results": [
            {
                "position": entry["position"],
                "driver": entry["driver"],
                "car": entry["car"],
                "total_time": entry["total_time"],
                "laps": entry["laps"]
            }
            for entry in entry_list
        ]
    }
    return results


def main():
    session_data = load_race_data(INPUT_FILE)
    results = simulate_race(session_data)
    print(json.dumps(results, indent=2))

    # Output results to file in data/sessions/
    output_dir = Path(__file__).parent.parent / "data" / "sessions"
    output_dir.mkdir(parents=True, exist_ok=True)
    # Use track name and date for filename (date can be generated here)
    from datetime import datetime
    track_name = results["track"]["name"].replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{timestamp}_{track_name}_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results written to {output_file}")


if __name__ == "__main__":
    main()
