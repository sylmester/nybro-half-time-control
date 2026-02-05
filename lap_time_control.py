#!/usr/bin/env python3
"""
Nybrogård Half Marathon Lap Time Control
A GUI application for recording lap times during a race.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import csv
from datetime import datetime
import os
import shutil
from pathlib import Path


class LapTimeControl:
    """Main application for controlling lap times."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Nybrogård Half Marathon - Lap Time Control")
        self.root.geometry("900x700")
        
        # Race state
        self.race_active = False
        self.runners = {}  # Dictionary: race_number -> runner_data
        self.lap_times = []  # List of lap time records
        self.total_laps = 0
        self.lap_length = 0.0
        self.runners_file = None
        self.output_file = None
        self.backup_counter = 0
        
        # Create GUI
        self.create_widgets()
        self.log_event("Application started")
        
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Top frame - Configuration
        config_frame = ttk.LabelFrame(self.root, text="Race Configuration", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Total laps
        ttk.Label(config_frame, text="Total Laps:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.total_laps_var = tk.IntVar(value=10)
        ttk.Entry(config_frame, textvariable=self.total_laps_var, width=10).grid(row=0, column=1, padx=5)
        
        # Lap length
        ttk.Label(config_frame, text="Lap Length (km):").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.lap_length_var = tk.DoubleVar(value=2.5)
        ttk.Entry(config_frame, textvariable=self.lap_length_var, width=10).grid(row=0, column=3, padx=5)
        
        # Load runners button
        ttk.Button(config_frame, text="Load Runners CSV", 
                  command=self.load_runners).grid(row=0, column=4, padx=5)
        
        self.runners_label = ttk.Label(config_frame, text="No runners loaded")
        self.runners_label.grid(row=0, column=5, padx=5)
        
        # Control frame - Start/Stop
        control_frame = ttk.LabelFrame(self.root, text="Race Control", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Race", 
                                       command=self.start_race, width=15)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Race", 
                                      command=self.stop_race, width=15, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.race_status_label = ttk.Label(control_frame, text="Race Status: Not Started", 
                                          font=('Arial', 10, 'bold'))
        self.race_status_label.pack(side=tk.LEFT, padx=20)
        
        # Input frame - Enter race numbers
        input_frame = ttk.LabelFrame(self.root, text="Record Lap Time", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Race Number:").pack(side=tk.LEFT, padx=5)
        self.race_number_var = tk.StringVar()
        self.race_number_entry = ttk.Entry(input_frame, textvariable=self.race_number_var, 
                                           width=15, font=('Arial', 12))
        self.race_number_entry.pack(side=tk.LEFT, padx=5)
        self.race_number_entry.bind('<Return>', lambda e: self.record_lap_time())
        
        ttk.Button(input_frame, text="Record Lap", 
                  command=self.record_lap_time).pack(side=tk.LEFT, padx=5)
        
        # Info frame - Show runner info
        info_frame = ttk.LabelFrame(self.root, text="Runner Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.runner_info_label = ttk.Label(info_frame, text="Enter a race number to see runner details", 
                                          font=('Arial', 10))
        self.runner_info_label.pack()
        
        # Log frame - Event log
        log_frame = ttk.LabelFrame(self.root, text="Event Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, 
                                                  font=('Courier', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def log_event(self, message):
        """Log an event to the GUI log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def load_runners(self):
        """Load runners from CSV file."""
        filename = filedialog.askopenfilename(
            title="Select Runners CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filename:
            return
            
        try:
            self.runners = {}
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    race_number = row.get('number', '').strip()
                    if race_number:
                        self.runners[race_number] = {
                            'number': race_number,
                            'hallway': row.get('hallway', '').strip(),
                            'gender': row.get('gender', '').strip(),
                            'laps': 0
                        }
            
            self.runners_file = filename
            count = len(self.runners)
            self.runners_label.config(text=f"{count} runners loaded")
            self.log_event(f"Loaded {count} runners from {os.path.basename(filename)}")
            self.status_bar.config(text=f"Loaded {count} runners")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load runners: {str(e)}")
            self.log_event(f"ERROR: Failed to load runners: {str(e)}")
            
    def start_race(self):
        """Start the race."""
        if not self.runners:
            messagebox.showwarning("Warning", "Please load runners before starting the race")
            return
            
        try:
            self.total_laps = self.total_laps_var.get()
            self.lap_length = self.lap_length_var.get()
            
            if self.total_laps <= 0 or self.lap_length <= 0:
                messagebox.showerror("Error", "Total laps and lap length must be positive")
                return
                
        except:
            messagebox.showerror("Error", "Invalid lap configuration")
            return
            
        # Create output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"lap_times_{timestamp}.csv"
        
        # Initialize output file
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'race_number', 'hallway', 'gender', 'lap_number', 'total_laps'])
        
        self.race_active = True
        self.lap_times = []
        self.backup_counter = 0
        
        # Reset lap counts
        for runner in self.runners.values():
            runner['laps'] = 0
            
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.race_status_label.config(text="Race Status: ACTIVE", foreground="green")
        
        self.log_event(f"Race started - {self.total_laps} laps x {self.lap_length} km")
        self.log_event(f"Output file: {self.output_file}")
        self.status_bar.config(text=f"Race active - Output: {self.output_file}")
        
        # Focus on race number entry
        self.race_number_entry.focus()
        
    def stop_race(self):
        """Stop the race."""
        if messagebox.askyesno("Confirm", "Are you sure you want to stop the race?"):
            self.race_active = False
            
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.race_status_label.config(text="Race Status: Stopped", foreground="red")
            
            # Create final backup
            self.create_backup()
            
            self.log_event("Race stopped")
            self.status_bar.config(text=f"Race stopped - Results saved to {self.output_file}")
            
    def record_lap_time(self):
        """Record a lap time for a runner."""
        if not self.race_active:
            messagebox.showwarning("Warning", "Race is not active")
            self.race_number_var.set("")
            return
            
        race_number = self.race_number_var.get().strip()
        
        if not race_number:
            return
            
        if race_number not in self.runners:
            messagebox.showwarning("Warning", f"Race number {race_number} not found")
            self.log_event(f"WARNING: Unknown race number: {race_number}")
            self.race_number_var.set("")
            return
            
        runner = self.runners[race_number]
        runner['laps'] += 1
        
        # Check if runner exceeded total laps
        if runner['laps'] > self.total_laps:
            messagebox.showwarning("Warning", 
                                 f"Runner {race_number} has already completed all {self.total_laps} laps")
            runner['laps'] = self.total_laps
            self.race_number_var.set("")
            return
            
        # Record lap time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        lap_record = {
            'timestamp': timestamp,
            'race_number': race_number,
            'hallway': runner['hallway'],
            'gender': runner['gender'],
            'lap_number': runner['laps'],
            'total_laps': self.total_laps
        }
        
        self.lap_times.append(lap_record)
        
        # Save to file
        with open(self.output_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                lap_record['timestamp'],
                lap_record['race_number'],
                lap_record['hallway'],
                lap_record['gender'],
                lap_record['lap_number'],
                lap_record['total_laps']
            ])
        
        # Update UI
        finish_text = " - FINISHED!" if runner['laps'] == self.total_laps else ""
        self.runner_info_label.config(
            text=f"Runner #{race_number} ({runner['hallway']}, {runner['gender']}) - "
                 f"Lap {runner['laps']}/{self.total_laps}{finish_text}"
        )
        
        self.log_event(f"Recorded: Runner #{race_number} - Lap {runner['laps']}/{self.total_laps}{finish_text}")
        
        # Clear input
        self.race_number_var.set("")
        
        # Create backup every 10 laps
        if len(self.lap_times) % 10 == 0:
            self.create_backup()
            
    def create_backup(self):
        """Create a backup of the lap times file."""
        if not self.output_file or not os.path.exists(self.output_file):
            return
            
        try:
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            self.backup_counter += 1
            backup_file = os.path.join(backup_dir, 
                                      f"backup_{self.backup_counter}_{os.path.basename(self.output_file)}")
            shutil.copy2(self.output_file, backup_file)
            
            self.log_event(f"Backup created: {backup_file}")
            
        except Exception as e:
            self.log_event(f"ERROR: Backup failed: {str(e)}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = LapTimeControl(root)
    root.mainloop()


if __name__ == "__main__":
    main()
