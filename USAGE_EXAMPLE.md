# Usage Example

This document provides a step-by-step example of using the Lap Time Control application.

## Scenario

You're organizing a half marathon with:
- 10 laps
- Each lap is 2.1 km (total 21 km = half marathon)
- 15 registered runners

## Step-by-Step Guide

### 1. Launch the Application

```bash
python3 lap_time_control.py
```

The application window opens with the following sections:
- Race Configuration (top)
- Race Control (start/stop buttons)
- Record Lap Time (input field)
- Runner Information (displays runner details)
- Event Log (scrollable log of all events)

### 2. Configure the Race

**In the Race Configuration section:**
- Total Laps: Enter `10`
- Lap Length (km): Enter `2.1`
- Click "Load Runners CSV"
- Select the `runners_sample.csv` file
- Status shows: "15 runners loaded"

**Event Log shows:**
```
[2024-01-15 09:00:00] Application started
[2024-01-15 09:00:15] Loaded 15 runners from runners_sample.csv
```

### 3. Start the Race

- Click the "Start Race" button
- The button becomes disabled
- "Stop Race" button becomes enabled
- Race Status changes to "ACTIVE" (in green)
- A new CSV file is created: `lap_times_20240115_090030.csv`

**Event Log shows:**
```
[2024-01-15 09:00:30] Race started - 10 laps x 2.1 km
[2024-01-15 09:00:30] Output file: lap_times_20240115_090030.csv
```

### 4. Record Lap Times

**First runner completes lap 1:**
- Enter race number: `101`
- Press Enter (or click "Record Lap")
- Runner Information displays: "Runner #101 (Nybrogård A, M) - Lap 1/10"

**Event Log shows:**
```
[2024-01-15 09:05:23] Recorded: Runner #101 - Lap 1/10
```

**Another runner completes lap 1:**
- Enter: `102`
- Press Enter
- Runner Information shows: "Runner #102 (Nybrogård A, F) - Lap 1/10"

**Continue recording as runners complete laps:**
- `103` → Lap 1/10
- `101` → Lap 2/10 (first runner's second lap)
- `104` → Lap 1/10
- ... and so on

**When runner completes final lap:**
- Enter: `101` (10th time)
- Runner Information shows: "Runner #101 (Nybrogård A, M) - Lap 10/10 - FINISHED!"

**Event Log shows:**
```
[2024-01-15 09:52:15] Recorded: Runner #101 - Lap 10/10 - FINISHED!
```

### 5. Automatic Backups

Every 10 lap recordings, a backup is automatically created:

**Event Log shows:**
```
[2024-01-15 09:15:30] Backup created: backups/backup_1_lap_times_20240115_090030.csv
[2024-01-15 09:25:45] Backup created: backups/backup_2_lap_times_20240115_090030.csv
```

### 6. Error Handling

**Unknown race number:**
- Enter: `999`
- Warning popup: "Race number 999 not found"
- Event Log: `[2024-01-15 09:20:00] WARNING: Unknown race number: 999`

**Exceeding total laps:**
- Runner #101 has completed 10 laps
- Enter: `101` again
- Warning popup: "Runner 101 has already completed all 10 laps"

### 7. Stop the Race

- Click "Stop Race" button
- Confirmation dialog: "Are you sure you want to stop the race?"
- Click "Yes"
- Race Status changes to "Stopped" (in red)
- Final backup is created

**Event Log shows:**
```
[2024-01-15 10:30:00] Backup created: backups/backup_5_lap_times_20240115_090030.csv
[2024-01-15 10:30:00] Race stopped
```

## Output File Format

The `lap_times_20240115_090030.csv` file contains:

```csv
timestamp,race_number,hallway,gender,lap_number,total_laps
2024-01-15 09:05:23.456,101,Nybrogård A,M,1,10
2024-01-15 09:06:12.123,102,Nybrogård A,F,1,10
2024-01-15 09:07:45.789,103,Nybrogård B,M,1,10
2024-01-15 09:10:15.234,101,Nybrogård A,M,2,10
2024-01-15 09:11:30.567,104,Nybrogård B,F,1,10
...
```

## Backups Directory Structure

```
backups/
├── backup_1_lap_times_20240115_090030.csv
├── backup_2_lap_times_20240115_090030.csv
├── backup_3_lap_times_20240115_090030.csv
├── backup_4_lap_times_20240115_090030.csv
└── backup_5_lap_times_20240115_090030.csv
```

## Tips

1. **Keep the window focused**: The race number input field automatically receives focus after each entry
2. **Use Enter key**: You can quickly enter race numbers using just the keyboard
3. **Monitor the log**: The event log shows all activities for transparency
4. **Check runner info**: After entering a number, verify the runner details are correct
5. **Regular backups**: Backups are automatic, but data is also saved immediately to the main file