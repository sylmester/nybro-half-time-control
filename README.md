# Nybrogård Half Marathon - Lap Time Control

Time control application for recording lap times at Nybrogård half marathon.

## Features

- **GUI-based lap time recording**: Easy-to-use interface for volunteers
- **Event logging**: All actions are logged in the GUI for transparency
- **Race configuration**: Specify total laps and lap length before starting
- **Runner management**: Load runner data from CSV file (number, hallway, gender)
- **Automatic saving**: Lap times are saved to CSV in real-time
- **Automatic backups**: Creates backups every 10 laps and when race is stopped

## Requirements

- Python 3.6 or higher (with tkinter support)

## Installation

No installation required. The application uses Python's standard library (tkinter, csv, datetime).

## Usage

1. **Start the application**:

   ```bash
   python3 lap_time_control.py
   ```

2. **Configure the race**:
   - Set the total number of laps
   - Set the lap length in kilometers
   - Load the runners CSV file (see format below)

3. **Start the race**:
   - Click "Start Race" button
   - The application will create a timestamped CSV file for lap times

4. **Record lap times**:
   - Enter the runner's race number in the input field
   - Press Enter or click "Record Lap"
   - The lap time is recorded with timestamp
   - Runner information is displayed
   - Event is logged

5. **Stop the race**:
   - Click "Stop Race" button
   - A final backup is created

## Runners CSV Format

The runners CSV file must have the following columns:

```csv
number,hallway,gender
101,Nybrogård A,M
102,Nybrogård A,F
103,Nybrogård B,M
```

- **number**: Race number (unique identifier)
- **hallway**: Runner's hallway/group
- **gender**: Runner's gender (M/F)

A sample file `runners_sample.csv` is provided.

## Output Format

Lap times are saved to a CSV file with the following format:

```csv
timestamp,race_number,hallway,gender,lap1,lap2, ... ,finish_time
2026-02-05 18:26:02.578,101,Nybrogård A,M,00:00:12.900,00:00:26.284, ... , 00:01:26.284
```

## Backups

Backups are automatically created:

- Every 10 recorded laps
- When the race is stopped

Backups are stored in the `backups/` directory with sequential numbering.
