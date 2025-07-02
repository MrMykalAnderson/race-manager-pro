# Race Manager Pro — Data Model

This document defines a flexible, extensible data model for representing race events, timing, results, and detailed car telemetry. The model is designed to be easily mapped to/from common standards (CSV, JSON, CAN, IRIG 106, etc.) and to support both simulation and real-world data.

---

## 1. Core Entities

### 1.1 Event
- `event_id`: Unique identifier
- `name`: Event name
- `date`: Date/time
- `location`: Track/circuit info
- `sessions`: List of Session objects

### 1.2 Session
- `session_id`: Unique identifier
- `type`: (Practice, Qualifying, Race, etc.)
- `start_time`, `end_time`
- `entries`: List of Entry objects
- `laps`: List of Lap objects
- `events`: List of EventLog objects

### 1.3 Entry (Car/Driver)
- `entry_id`: Unique identifier
- `car_number`, `team`, `driver`, `car_model`
- `class`: (if multi-class)
- `status`: (active, retired, DNF, etc.)

### 1.4 Lap
- `lap_number`
- `entry_id`: Reference to Entry
- `lap_time`
- `sector_times`: List of sector times
- `pit_stop`: Boolean or pit stop details
- `telemetry`: List of TelemetrySample objects (optional, for detailed data)

### 1.5 TelemetrySample
- `timestamp`
- `speed`, `rpm`, `throttle`, `brake`, `gear`, `g_force`, `steering_angle`, `tire_temps`, etc.
- (Extensible: add more fields as needed)

### 1.6 EventLog
- `timestamp`
- `type`: (penalty, incident, pit stop, etc.)
- `description`
- `affected_entries`: List of entry_ids

---

## 2. Example (JSON)
```json
{
  "event_id": "2025-austrian-gp",
  "name": "Austrian Grand Prix",
  "date": "2025-06-29T14:00:00Z",
  "location": "Red Bull Ring",
  "sessions": [
    {
      "session_id": "race",
      "type": "Race",
      "start_time": "2025-06-29T14:00:00Z",
      "entries": [
        {"entry_id": "car44", "car_number": 44, "team": "Mercedes", "driver": "Lewis Hamilton", "status": "active"}
      ],
      "laps": [
        {"lap_number": 1, "entry_id": "car44", "lap_time": "1:32.456", "sector_times": ["0:30.123", "0:31.456", "0:30.877"], "telemetry": [
          {"timestamp": 123456789, "speed": 312, "rpm": 12000, "throttle": 0.98, "brake": 0.0, "gear": 7}
        ]}
      ],
      "events": [
        {"timestamp": "2025-06-29T14:15:00Z", "type": "pit_stop", "description": "Car 44 pit stop", "affected_entries": ["car44"]}
      ]
    }
  ]
}
```

---

## 3. Implementation Notes
- The current implementation uses a simplified model for simulation and results, as seen in `dev/SAMPLE_4_CAR_RACE.json` and session result files.
- These files use top-level keys like `track`, `cars`, `drivers`, `entries`, and `results`.
- The model is designed to be extended toward the full structure described above as more features are implemented.
- See `dev/SAMPLE_4_CAR_RACE.json` for a concrete example of the current data structure.

---

## 4. Extensibility
- Add new fields as needed for new data types (e.g., weather, tire compounds, strategy calls).
- Use references (IDs) to link related entities.
- Store high-frequency telemetry as separate files if needed, with references in the main data structure.

---

*This model is a living document. Update as requirements evolve or new standards emerge.*
