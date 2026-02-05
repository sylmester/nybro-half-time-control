# GUI Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Nybrogård Half Marathon - Lap Time Control                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌─ Race Configuration ────────────────────────────────────────────────┐ │
│ │                                                                      │ │
│ │  Total Laps: [10    ]  Lap Length (km): [2.5    ]                   │ │
│ │                                                                      │ │
│ │  [Load Runners CSV]  15 runners loaded                              │ │
│ │                                                                      │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─ Race Control ──────────────────────────────────────────────────────┐ │
│ │                                                                      │ │
│ │  [Start Race]  [Stop Race]    Race Status: ACTIVE                   │ │
│ │                                                                      │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─ Record Lap Time ───────────────────────────────────────────────────┐ │
│ │                                                                      │ │
│ │  Race Number:  [101         ]  [Record Lap]                         │ │
│ │                                                                      │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─ Runner Information ────────────────────────────────────────────────┐ │
│ │                                                                      │ │
│ │  Runner #101 (Nybrogård A, M) - Lap 3/10                            │ │
│ │                                                                      │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─ Event Log ─────────────────────────────────────────────────────────┐ │
│ │ [2024-01-15 09:00:00] Application started                          │ │
│ │ [2024-01-15 09:00:15] Loaded 15 runners from runners_sample.csv    │ │
│ │ [2024-01-15 09:00:30] Race started - 10 laps x 2.5 km              │ │
│ │ [2024-01-15 09:00:30] Output file: lap_times_20240115_090030.csv   │ │
│ │ [2024-01-15 09:05:23] Recorded: Runner #101 - Lap 1/10             │ │
│ │ [2024-01-15 09:06:12] Recorded: Runner #102 - Lap 1/10             │ │
│ │ [2024-01-15 09:07:45] Recorded: Runner #103 - Lap 1/10             │ │
│ │ [2024-01-15 09:10:15] Recorded: Runner #101 - Lap 2/10             │ │
│ │ [2024-01-15 09:11:30] Recorded: Runner #104 - Lap 1/10             │ │
│ │ [2024-01-15 09:15:30] Backup created: backups/backup_1_lap_...     │ │
│ │ [2024-01-15 09:18:45] Recorded: Runner #101 - Lap 3/10             │ │
│ │                                                 ▲                   │ │
│ │                                                 │                   │ │
│ │                                            Scroll Bar               │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Ready                                                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

## GUI Components

### 1. Race Configuration Section
- **Total Laps**: Input field for number of laps in the race
- **Lap Length**: Input field for the length of each lap in kilometers
- **Load Runners CSV**: Button to load the runners data file
- **Status Label**: Shows how many runners are loaded

### 2. Race Control Section
- **Start Race**: Button to start the race (creates output file)
- **Stop Race**: Button to stop the race (creates final backup)
- **Race Status**: Visual indicator showing current race state (Not Started / ACTIVE / Stopped)

### 3. Record Lap Time Section
- **Race Number**: Input field for entering runner's race number
- **Record Lap**: Button to record the lap time (or press Enter)
- Focus automatically returns to this field after each entry for fast data entry

### 4. Runner Information Section
- Displays details about the last runner whose lap was recorded
- Shows: race number, hallway, gender, current lap, total laps
- Shows "FINISHED!" when runner completes all laps

### 5. Event Log Section
- Scrollable text area showing all events
- Each event is timestamped
- Logs include:
  - Application lifecycle events (start, stop)
  - Runner file loading
  - Race control actions
  - Lap recordings
  - Backup creation
  - Warnings and errors

### 6. Status Bar
- Bottom bar showing current application status

## Color Scheme

- **Race Status (Active)**: Green text
- **Race Status (Stopped)**: Red text
- **Event Log**: Monospace font for easy reading
- **Input Field**: Large font (12pt) for quick entry

## Keyboard Shortcuts

- **Enter**: Record lap time (when focus is in race number field)
- **Tab**: Navigate between input fields
- Race number field automatically receives focus after recording
