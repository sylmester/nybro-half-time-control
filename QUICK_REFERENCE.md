# Quick Reference Card for Volunteers

## Before the Race

1. **Start the application**: 
   ```bash
   python3 lap_time_control.py
   ```

2. **Configure settings**:
   - Total Laps: _____ (e.g., 10)
   - Lap Length: _____ km (e.g., 2.1)

3. **Load runners**: Click "Load Runners CSV" and select the file

4. **Start race**: Click "Start Race" button

## During the Race

### Recording Lap Times (Fast Entry)

1. Type race number
2. Press **Enter**
3. Repeat

**That's it!** The system automatically:
- Records the timestamp
- Saves to CSV file
- Shows runner info
- Logs the event
- Creates backups every 10 laps

### What You'll See

After entering a race number:
- **Runner Info** shows: "Runner #101 (Nybrogård A, M) - Lap 3/10"
- **Event Log** shows: "[Time] Recorded: Runner #101 - Lap 3/10"

When a runner finishes:
- Info shows: "... - Lap 10/10 - FINISHED!"

### Error Messages

| Message | Meaning | Action |
|---------|---------|--------|
| "Race number XXX not found" | Unknown runner | Check the number, ask runner |
| "Already completed all laps" | Runner finished | Don't record again |
| "Race is not active" | Race not started | Click "Start Race" first |

## After the Race

1. Click "Stop Race"
2. Confirm by clicking "Yes"
3. Done! All data is saved

## Files Generated

- **Main file**: `lap_times_YYYYMMDD_HHMMSS.csv` - All lap times
- **Backups**: `backups/backup_N_lap_times_*.csv` - Automatic backups

## Tips

✓ Keep window focused on the race number field
✓ Use keyboard only for fastest entry (Enter key)
✓ Watch the Event Log to confirm each entry
✓ If unsure, check Runner Information panel
✓ Backups happen automatically - don't worry!

## Emergency

If something goes wrong:
1. Don't panic - data is saved after each lap
2. Check the backups folder
3. Check the Event Log for errors
4. The main CSV file has all recorded laps

## Support

Check the Event Log at the bottom of the window for detailed information about what's happening.
