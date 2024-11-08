import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class TOTCalculator: #sunshine is gay
    def __init__(self, root):
        self.root = root
        self.root.title("Time on Target (TOT) Calculator")
        
        # Input Variables
        self.start_time_var = tk.StringVar()
        self.tot_offset_var = tk.StringVar()
        self.ground_speed_var = tk.StringVar()
        self.altitude_var = tk.StringVar()
        self.hold_distance_var = tk.StringVar()
        self.release_distance_var = tk.StringVar()
        self.bomb_time_var = tk.StringVar()
        self.additional_distance_var = tk.StringVar()
        self.tot_window_var = tk.StringVar(value="±3")
        
        # Build GUI
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Start Time (HH:MM):").grid(row=0, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.start_time_var).grid(row=0, column=1)
        
        tk.Label(self.root, text="TOT Offset (minutes):").grid(row=1, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.tot_offset_var).grid(row=1, column=1)
        
        tk.Label(self.root, text="Ground Speed (knots):").grid(row=2, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.ground_speed_var).grid(row=2, column=1)
        
        tk.Label(self.root, text="Altitude (feet):").grid(row=3, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.altitude_var).grid(row=3, column=1)
        
        tk.Label(self.root, text="Hold Distance to Target (NM):").grid(row=4, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.hold_distance_var).grid(row=4, column=1)
        
        tk.Label(self.root, text="Bomb Release Distance (NM):").grid(row=5, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.release_distance_var).grid(row=5, column=1)
        
        tk.Label(self.root, text="Bomb Time of Fall (seconds):").grid(row=6, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.bomb_time_var).grid(row=6, column=1)
        
        tk.Label(self.root, text="Additional Distance (NM, optional):").grid(row=7, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.additional_distance_var).grid(row=7, column=1)
        
        tk.Label(self.root, text="TOT Window (seconds):").grid(row=8, column=0, sticky=tk.E)
        tk.Entry(self.root, textvariable=self.tot_window_var).grid(row=8, column=1)
        
        tk.Button(self.root, text="Calculate", command=self.calculate_tot).grid(row=9, column=0, columnspan=2)
        
        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.grid(row=10, column=0, columnspan=2)
    
    def calculate_tot(self):
        try:
            # Parse Input Values
            start_time_str = self.start_time_var.get()
            tot_offset = int(self.tot_offset_var.get())
            ground_speed = float(self.ground_speed_var.get())
            altitude = float(self.altitude_var.get())
            hold_distance = float(self.hold_distance_var.get())
            release_distance = float(self.release_distance_var.get())
            bomb_time_of_fall = float(self.bomb_time_var.get())
            additional_distance = self.additional_distance_var.get()
            tot_window = int(self.tot_window_var.get().replace('±', ''))
            
            # Calculate TOT
            start_time = datetime.strptime(start_time_str, "%H:%M")
            tot = start_time + timedelta(minutes=tot_offset)
            tot_str = tot.strftime("%H:%M:%S")
            
            # Adjust Hold Distance if Additional Distance is provided
            if additional_distance:
                hold_distance += float(additional_distance)
            
            # Calculate Distances and Times
            distance_to_release = hold_distance - release_distance
            time_to_release = (distance_to_release / ground_speed) * 3600  # seconds
            total_time = time_to_release + bomb_time_of_fall  # seconds
            
            # Calculate Departure Time from Hold
            departure_time = tot - timedelta(seconds=total_time)
            departure_time_str = departure_time.strftime("%H:%M:%S")
            
            # Calculate Bomb Release Time
            bomb_release_time = departure_time + timedelta(seconds=time_to_release)
            bomb_release_time_str = bomb_release_time.strftime("%H:%M:%S")
            
            # Output Results
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Time on Target (TOT): {tot_str}\n")
            self.output_text.insert(tk.END, f"Departure Time from Hold: {departure_time_str}\n")
            self.output_text.insert(tk.END, f"Time at Bomb Release: {bomb_release_time_str}\n")
            self.output_text.insert(tk.END, f"Total Time from Hold to Target Impact: {int(total_time)} seconds\n")
            self.output_text.insert(tk.END, f"Within TOT Window: ±{tot_window} seconds\n")
        except Exception as e:
            messagebox.showerror("Input Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TOTCalculator(root)
    root.mainloop()
