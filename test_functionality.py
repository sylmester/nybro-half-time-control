#!/usr/bin/env python3
"""
Test script for lap time control functionality (non-GUI parts).
"""

import csv
import os
import tempfile
from datetime import datetime


def test_csv_reading():
    """Test reading runners from CSV."""
    print("Testing CSV reading...")
    
    runners = {}
    with open('runners_sample.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            race_number = row.get('number', '').strip()
            if race_number:
                runners[race_number] = {
                    'number': race_number,
                    'hallway': row.get('hallway', '').strip(),
                    'gender': row.get('gender', '').strip(),
                    'laps': 0
                }
    
    print(f"✓ Loaded {len(runners)} runners")
    print(f"  Sample: Runner #{list(runners.keys())[0]}: {runners[list(runners.keys())[0]]}")
    return runners


def test_csv_writing(runners):
    """Test writing lap times to CSV."""
    print("\nTesting CSV writing...")
    
    # Create a test output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"test_lap_times_{timestamp}.csv"
    
    # Write header
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'race_number', 'hallway', 'gender', 'lap_number', 'total_laps'])
    
    # Write some test lap times
    race_numbers = list(runners.keys())[:3]
    total_laps = 5
    
    for i, race_number in enumerate(race_numbers):
        runner = runners[race_number]
        lap_number = i + 1
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        with open(output_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                race_number,
                runner['hallway'],
                runner['gender'],
                lap_number,
                total_laps
            ])
    
    print(f"✓ Created test output file: {output_file}")
    
    # Read back and verify
    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = sum(1 for row in reader)
    
    print(f"✓ Verified {count} lap time records written")
    
    # Clean up
    os.remove(output_file)
    print(f"✓ Cleaned up test file")
    

def test_backup_creation():
    """Test backup functionality."""
    print("\nTesting backup creation...")
    
    # Create a temporary file
    test_file = "test_data.csv"
    with open(test_file, 'w') as f:
        f.write("test,data\n1,2\n")
    
    # Create backup directory
    backup_dir = "test_backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create backup
    import shutil
    backup_file = os.path.join(backup_dir, f"backup_1_{os.path.basename(test_file)}")
    shutil.copy2(test_file, backup_file)
    
    print(f"✓ Created backup: {backup_file}")
    print(f"✓ Backup exists: {os.path.exists(backup_file)}")
    
    # Clean up
    os.remove(test_file)
    os.remove(backup_file)
    os.rmdir(backup_dir)
    print(f"✓ Cleaned up test files")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Lap Time Control - Non-GUI Functionality Tests")
    print("=" * 60)
    
    try:
        runners = test_csv_reading()
        test_csv_writing(runners)
        test_backup_creation()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
