import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WaterIntakeTracker:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("Water Intake Tracker")
        self.root.geometry("500x700")
        self.root.configure(bg="#e6f7ff")
        
        # Set default values
        self.goal = 2000  # Default goal in ml
        self.intake = 0   # Current intake in ml
        self.log = []     # Log of today's water intake entries
        self.history = [] # History of previous days
        
        # Load saved data if it exists
        self.load_data()
        
        # Create and display UI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI elements for the water tracker"""
        # Title label
        title_label = tk.Label(
            self.root, 
            text="Water Intake Tracker", 
            font=("Arial", 18, "bold"),
            bg="#e6f7ff",
            fg="#0066cc"
        )
        title_label.pack(pady=10)
        
        # Date label
        date_label = tk.Label(
            self.root,
            text=datetime.now().strftime("%A, %B %d, %Y"),
            font=("Arial", 12),
            bg="#e6f7ff",
            fg="#0066cc"
        )
        date_label.pack(pady=5)
        
        # Progress frame
        progress_frame = tk.Frame(self.root, bg="#e6f7ff")
        progress_frame.pack(pady=15)
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=self.calculate_progress())
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            orient="horizontal",
            length=300,
            mode="determinate",
            maximum=100
        )
        self.progress_bar.grid(row=0, column=0, padx=10, pady=10)
        
        # Progress text
        self.progress_text = tk.Label(
            progress_frame,
            text=f"{self.intake} ml of {self.goal} ml ({int(self.calculate_progress())}%)",
            font=("Arial", 10),
            bg="#e6f7ff"
        )
        self.progress_text.grid(row=1, column=0, padx=10)
        
        # Goal setting frame
        goal_frame = tk.Frame(self.root, bg="#e6f7ff")
        goal_frame.pack(pady=10)
        
        # Goal label
        goal_label = tk.Label(
            goal_frame,
            text="Daily Goal (ml):",
            font=("Arial", 12),
            bg="#e6f7ff"
        )
        goal_label.grid(row=0, column=0, padx=5)
        
        # Goal entry
        self.goal_var = tk.IntVar(value=self.goal)
        goal_entry = tk.Entry(
            goal_frame,
            textvariable=self.goal_var,
            width=6,
            font=("Arial", 12)
        )
        goal_entry.grid(row=0, column=1, padx=5)
        
        # Update goal button
        update_goal_button = tk.Button(
            goal_frame,
            text="Update Goal",
            command=self.update_goal,
            bg="#3399ff",
            fg="white",
            font=("Arial", 10),
            padx=5
        )
        update_goal_button.grid(row=0, column=2, padx=5)
        
        # Water intake buttons frame
        buttons_frame = tk.Frame(self.root, bg="#e6f7ff")
        buttons_frame.pack(pady=10)
        
        # Add 250ml button
        add_250_button = tk.Button(
            buttons_frame,
            text="Add 250ml",
            command=lambda: self.add_water(250),
            bg="#3399ff",
            fg="white",
            font=("Arial", 12),
            width=10,
            height=2
        )
        add_250_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Add 500ml button
        add_500_button = tk.Button(
            buttons_frame,
            text="Add 500ml",
            command=lambda: self.add_water(500),
            bg="#3399ff",
            fg="white",
            font=("Arial", 12),
            width=10,
            height=2
        )
        add_500_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Remove 250ml button
        remove_button = tk.Button(
            buttons_frame,
            text="Remove 250ml",
            command=lambda: self.remove_water(250),
            bg="#ff9999",
            fg="white",
            font=("Arial", 12),
            width=10,
            height=2
        )
        remove_button.grid(row=1, column=0, padx=5, pady=5)
        
        # Reset button
        reset_button = tk.Button(
            buttons_frame,
            text="Reset Day",
            command=self.reset_day,
            bg="#ff6666",
            fg="white",
            font=("Arial", 12),
            width=10,
            height=2
        )
        reset_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Custom amount frame
        custom_frame = tk.Frame(self.root, bg="#e6f7ff")
        custom_frame.pack(pady=10)
        
        # Custom amount label
        custom_label = tk.Label(
            custom_frame,
            text="Custom Amount (ml):",
            font=("Arial", 12),
            bg="#e6f7ff"
        )
        custom_label.grid(row=0, column=0, padx=5)
        
        # Custom amount entry
        self.custom_var = tk.StringVar()
        custom_entry = tk.Entry(
            custom_frame,
            textvariable=self.custom_var,
            width=8,
            font=("Arial", 12)
        )
        custom_entry.grid(row=0, column=1, padx=5)
        
        # Custom amount add button
        custom_button = tk.Button(
            custom_frame,
            text="Add",
            command=self.add_custom,
            bg="#3399ff",
            fg="white",
            font=("Arial", 10),
            padx=10
        )
        custom_button.grid(row=0, column=2, padx=5)
        
        # Today's log label
        log_label = tk.Label(
            self.root,
            text="Today's Log",
            font=("Arial", 14, "bold"),
            bg="#e6f7ff",
            fg="#0066cc"
        )
        log_label.pack(pady=(15, 5))
        
        # Log frame with scrollbar
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=20)
        
        # Scrollbar for log
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Log listbox
        self.log_listbox = tk.Listbox(
            log_frame,
            height=8,
            width=50,
            font=("Arial", 10),
            yscrollcommand=scrollbar.set
        )
        self.log_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_listbox.yview)
        
        # History label (only shown if there's history)
        if self.history:
            history_label = tk.Label(
                self.root,
                text="Previous Days",
                font=("Arial", 14, "bold"),
                bg="#e6f7ff",
                fg="#0066cc"
            )
            history_label.pack(pady=(15, 5))
            
            # History frame with scrollbar
            history_frame = tk.Frame(self.root)
            history_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=20)
            
            # Scrollbar for history
            history_scrollbar = tk.Scrollbar(history_frame)
            history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # History listbox
            self.history_listbox = tk.Listbox(
                history_frame,
                height=6,
                width=50,
                font=("Arial", 10),
                yscrollcommand=history_scrollbar.set
            )
            self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            history_scrollbar.config(command=self.history_listbox.yview)
            
            # Populate history listbox
            self.update_history_display()
        
        # Update log display
        self.update_log_display()
        
    def calculate_progress(self):
        """Calculate the progress percentage"""
        if self.goal <= 0:
            return 0
        progress = (self.intake / self.goal) * 100
        return min(progress, 100)  # Cap at 100%
        
    def update_goal(self):
        """Update the daily water intake goal"""
        try:
            new_goal = self.goal_var.get()
            if new_goal <= 0:
                messagebox.showerror("Invalid Goal", "Goal must be greater than zero.")
                self.goal_var.set(self.goal)  # Reset to current goal
                return
                
            self.goal = new_goal
            self.update_progress_display()
            self.save_data()
            messagebox.showinfo("Goal Updated", f"Daily goal updated to {self.goal} ml.")
        except tk.TclError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            self.goal_var.set(self.goal)  # Reset to current goal
    
    def add_water(self, amount):
        """Add water to the daily intake"""
        self.intake += amount
        
        # Add to log
        now = datetime.now().strftime("%H:%M")
        self.log.append({
            "time": now,
            "amount": amount,
            "total": self.intake
        })
        
        self.update_progress_display()
        self.update_log_display()
        self.save_data()
        
        # Check if goal reached
        if self.calculate_progress() >= 100 and amount > 0:
            messagebox.showinfo("Goal Reached", "Congratulations! You've reached your daily water goal!")
    
    def remove_water(self, amount):
        """Remove water from the daily intake"""
        if self.intake >= amount:
            self.intake -= amount
            
            # Add to log with negative amount
            now = datetime.now().strftime("%H:%M")
            self.log.append({
                "time": now,
                "amount": -amount,
                "total": self.intake
            })
            
            self.update_progress_display()
            self.update_log_display()
            self.save_data()
        else:
            messagebox.showerror("Error", "Cannot remove more than current intake.")
    
    def add_custom(self):
        """Add custom amount of water"""
        try:
            amount = int(self.custom_var.get())
            if amount <= 0:
                messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
                return
                
            self.add_water(amount)
            self.custom_var.set("")  # Clear the entry
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    def reset_day(self):
        """Reset the day's water intake"""
        if self.intake > 0:
            if messagebox.askyesno("Reset Day", "Are you sure you want to reset today's data?"):
                # Add to history before resetting
                today = datetime.now().strftime("%Y-%m-%d")
                self.history.append({
                    "date": today,
                    "intake": self.intake,
                    "goal": self.goal
                })
                
                # Reset intake and log
                self.intake = 0
                self.log = []
                
                self.update_progress_display()
                self.update_log_display()
                self.update_history_display()
                self.save_data()
        else:
            messagebox.showinfo("Reset Day", "No water intake to reset.")
    
    def update_progress_display(self):
        """Update the progress bar and text"""
        progress = self.calculate_progress()
        self.progress_var.set(progress)
        self.progress_text.config(text=f"{self.intake} ml of {self.goal} ml ({int(progress)}%)")
    
    def update_log_display(self):
        """Update the log listbox"""
        self.log_listbox.delete(0, tk.END)  # Clear current list
        
        if not self.log:
            self.log_listbox.insert(tk.END, "No entries yet today.")
            return
            
        # Add column headers
        self.log_listbox.insert(tk.END, f"{'Time':<10}{'Amount':<15}{'Total':<15}")
        self.log_listbox.insert(tk.END, "-" * 40)
        
        # Add log entries
        for entry in self.log:
            sign = "+" if entry["amount"] > 0 else ""
            self.log_listbox.insert(
                tk.END, 
                f"{entry['time']:<10}{sign}{entry['amount']} ml{'':<5}{entry['total']} ml"
            )
    
    def update_history_display(self):
        """Update the history listbox"""
        if not hasattr(self, 'history_listbox'):
            return
            
        self.history_listbox.delete(0, tk.END)  # Clear current list
        
        if not self.history:
            self.history_listbox.insert(tk.END, "No history available.")
            return
            
        # Add column headers
        self.history_listbox.insert(tk.END, f"{'Date':<12}{'Intake':<12}{'Goal':<12}{'Percentage':<10}")
        self.history_listbox.insert(tk.END, "-" * 46)
        
        # Add history entries (most recent first)
        for entry in reversed(self.history):
            percentage = int((entry["intake"] / entry["goal"]) * 100) if entry["goal"] > 0 else 0
            self.history_listbox.insert(
                tk.END, 
                f"{entry['date']:<12}{entry['intake']} ml{'':<4}{entry['goal']} ml{'':<4}{percentage}%"
            )
    
    def load_data(self):
        """Load saved data from file"""
        try:
            if os.path.exists("water_tracker_data.json"):
                with open("water_tracker_data.json", "r") as file:
                    data = json.load(file)
                    
                    # Get saved goal
                    self.goal = data.get("goal", 2000)
                    
                    # Check if the saved date is today
                    last_date = data.get("date", "")
                    today = datetime.now().strftime("%Y-%m-%d")
                    
                    if last_date == today:
                        # Continue from today's data
                        self.intake = data.get("intake", 0)
                        self.log = data.get("log", [])
                    else:
                        # It's a new day, move previous day to history if there was intake
                        if "intake" in data and data["intake"] > 0:
                            self.history = data.get("history", [])
                            self.history.append({
                                "date": last_date,
                                "intake": data["intake"],
                                "goal": data.get("goal", 2000)
                            })
                        else:
                            self.history = data.get("history", [])
                            
                        # Reset for today
                        self.intake = 0
                        self.log = []
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save data to file"""
        try:
            data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "goal": self.goal,
                "intake": self.intake,
                "log": self.log,
                "history": self.history
            }
            
            with open("water_tracker_data.json", "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error saving data: {e}")

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = WaterIntakeTracker(root)
    
    # Set icon (uncomment and provide path to an icon file if you have one)
    # root.iconbitmap("water_icon.ico")
    
    # Start the application
    root.mainloop()
