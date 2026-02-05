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
        self.race_start_time = None
        self.race_start_timestamp = None
        self.runner_laps = {}  # race_number -> list of elapsed lap times (HH:MM:SS.mmm)
        
        # Create GUI
        self.create_widgets()
        self.log_event("Application started")
        
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Main padded container to give edge padding
        self.main_container = ttk.Frame(self.root, padding=10)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Configure ttk styles for colored buttons (macOS-friendly using 'clam' theme)
        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('Success.TButton', foreground='white', background='#28a745', padding=6)
        style.map('Success.TButton',
                  background=[('active', '#218838'), ('pressed', '#1e7e34')],
                  foreground=[('disabled', '#cccccc')])
        style.configure('Danger.TButton', foreground='white', background='#dc3545', padding=6)
        style.map('Danger.TButton',
                  background=[('active', '#c82333'), ('pressed', '#bd2130')],
                  foreground=[('disabled', '#cccccc')])
        style.configure('Primary.TButton', foreground='white', background='#007bff', padding=6)
        style.map('Primary.TButton',
                  background=[('active', '#0056b3'), ('pressed', '#004085')],
                  foreground=[('disabled', '#cccccc')])

        # Top frame - Configuration
        config_frame = ttk.LabelFrame(self.main_container, text="Race Configuration", padding=10)
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
        control_frame = ttk.LabelFrame(self.main_container, text="Race Control", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Colored buttons using ttk with custom styles
        self.start_button = ttk.Button(control_frame, text="Start Race",
                           command=self.start_race, width=15, style='Success.TButton')
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Race",
                          command=self.stop_race, width=15, state=tk.DISABLED, style='Danger.TButton')
        self.stop_button.pack(side=tk.LEFT, padx=5)

        
        
        self.race_status_label = ttk.Label(control_frame, text="Race Status: Not Started", 
                                          font=('Arial', 10, 'bold'))
        self.race_status_label.pack(side=tk.LEFT, padx=20)

        # Race timer label
        self.race_timer_label = ttk.Label(control_frame, text="Race Time: 00:00:00", 
                                          font=('Arial', 12, 'bold'))
        self.race_timer_label.pack(side=tk.RIGHT, padx=10)
        
        # Input frame - Enter race numbers
        input_frame = ttk.LabelFrame(self.main_container, text="Record Lap Time", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Race Number:").pack(side=tk.LEFT, padx=5)
        self.race_number_var = tk.StringVar()
        self.race_number_entry = ttk.Entry(input_frame, textvariable=self.race_number_var, 
                                           width=15, font=('Arial', 12))
        self.race_number_entry.pack(side=tk.LEFT, padx=5)
        self.race_number_entry.bind('<Return>', lambda e: self.record_lap_time())
        
        self.record_button = ttk.Button(input_frame, text="Record Lap",
                        command=self.record_lap_time, style='Primary.TButton')
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        # Info frame - Show runner info
        info_frame = ttk.LabelFrame(self.main_container, text="Runner Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.runner_info_label = ttk.Label(info_frame, text="Enter a race number to see runner details", 
                                          font=('Arial', 10))
        self.runner_info_label.pack()
        
        # Log frame - Event log
        log_frame = ttk.LabelFrame(self.main_container, text="Event Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, 
                                                  font=('Courier', 12))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        # Tag for error/wrong number entries
        self.log_text.tag_config('error', foreground='red')
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def log_event(self, message, color=None):
        """Log an event to the GUI log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        if color:
            # Ensure tag exists; use provided color name as tag
            try:
                self.log_text.insert(tk.END, log_message, (color,))
            except tk.TclError:
                # Fallback: configure tag dynamically and insert
                self.log_text.tag_config(color, foreground=color)
                self.log_text.insert(tk.END, log_message, (color,))
        else:
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
        self.race_start_time = datetime.now()
        self.race_start_timestamp = self.race_start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # Initialize output file with new header: timestamp,race_number,hallway,gender,lap1..lapN,finish_time
        header = ['timestamp', 'race_number', 'hallway', 'gender'] + \
                 [f'lap{i}' for i in range(1, self.total_laps + 1)] + ['finish_time']
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        
        self.race_active = True
        self.lap_times = []
        self.backup_counter = 0
        self.runner_laps = {}
        
        # Reset lap counts
        for runner in self.runners.values():
            runner['laps'] = 0
            
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.race_status_label.config(text="Race Status: ACTIVE", foreground="green")
        self.race_timer_label.config(text="Race Time: 00:00:00")
        self.update_timer()
        
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
            self.log_event(f"WARNING: Unknown race number: {race_number}", color='error')
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
            
        # Record lap elapsed time since race start
        now = datetime.now()
        elapsed_str = self._format_elapsed(now - self.race_start_time)
        self.runner_laps.setdefault(race_number, []).append(elapsed_str)
        
        # Track for backup cadence
        self.lap_times.append({
            'timestamp': now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            'race_number': race_number,
            'lap_number': runner['laps']
        })
        
        # Save entire CSV in new format
        self.save_results_csv()
        
        # Update UI
        finish_text = " - FINISHED!" if runner['laps'] == self.total_laps else ""
        self.runner_info_label.config(
            text=f"Runner #{race_number} ({runner['hallway']}, {runner['gender']}) - "
                 f"Lap {runner['laps']}/{self.total_laps} at {elapsed_str}{finish_text}"
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

    def _format_elapsed(self, delta):
        """Format a timedelta as HH:MM:SS.mmm"""
        total_ms = int(delta.total_seconds() * 1000)
        hours = total_ms // (3600 * 1000)
        minutes = (total_ms // (60 * 1000)) % 60
        seconds = (total_ms // 1000) % 60
        ms = total_ms % 1000
        return f"{hours:02}:{minutes:02}:{seconds:02}.{ms:03}"

    def update_timer(self):
        """Update race timer label while race is active."""
        if self.race_active and self.race_start_time:
            now = datetime.now()
            elapsed_str = self._format_elapsed(now - self.race_start_time)
            self.race_timer_label.config(text=f"Race Time: {elapsed_str}")
            # Refresh ~10 times per second
            self.root.after(100, self.update_timer)

    def save_results_csv(self):
        """Rewrite the CSV with header and per-runner lap columns."""
        if not self.output_file:
            return
        header = (
            ['timestamp', 'race_number', 'hallway', 'gender'] +
            [f'lap{i}' for i in range(1, self.total_laps + 1)] + ['finish_time']
        )
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for race_number, laps in self.runner_laps.items():
                    runner = self.runners.get(race_number, {})
                    hallway = runner.get('hallway', '')
                    gender = runner.get('gender', '')
                    row = [self.race_start_timestamp, race_number, hallway, gender]
                    # Add lap columns padded to total_laps
                    lap_cols = laps[:self.total_laps] + [''] * max(0, self.total_laps - len(laps))
                    row.extend(lap_cols)
                    finish_time = laps[self.total_laps - 1] if len(laps) >= self.total_laps else ''
                    row.append(finish_time)
                    writer.writerow(row)
        except Exception as e:
            self.log_event(f"ERROR: Failed to save CSV: {str(e)}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = LapTimeControl(root)
    root.mainloop()


if __name__ == "__main__":
    main()
