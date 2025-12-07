import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
from tkcalendar import Calendar
from data_manager import CalendarDataManager

class CalendarApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Calendar & Timetable")
        self.geometry("1000x700")
        self.resizable(True, True)
       
        # Set window icon (using the same icon as main_app)
        self.set_window_icon()
       
        # Initialize events data storage
        self.events = {}
        self.data_file = "calendar_events.json"
        self.current_date = datetime.now().strftime("%Y-%m-%d")
       
        # Load existing events from storage
        self.load_events()
       
        # Create and setup GUI components
        self.create_widgets()
       
        # Bind window close event handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)
       
        # Display events for current date
        self.show_date_events(self.current_date)
   
    def set_window_icon(self):
        """Set window icon (consistent with main_app)"""
        icon_paths = [
            "icon.ico",           # Windows icon
            "assets/icon.ico",    # In assets folder
            "images/icon.ico",    # In images folder
            "icon.png",           # PNG format
            "assets/icon.png",    # PNG in assets
            "images/icon.png"     # PNG in images
        ]
       
        for icon_path in icon_paths:
            try:
                if os.path.exists(icon_path):
                    if icon_path.endswith('.ico'):
                        self.iconbitmap(icon_path)
                        print(f"Calendar App icon set from: {icon_path}")
                        return
                    elif icon_path.endswith(('.png', '.jpg', '.gif')):
                        # For image files, use iconphoto
                        from PIL import Image, ImageTk
                        icon_image = Image.open(icon_path)
                        icon_photo = ImageTk.PhotoImage(icon_image)
                        self.iconphoto(False, icon_photo)
                        print(f"Calendar App icon set from: {icon_path}")
                        return
            except Exception as e:
                print(f"Error loading icon {icon_path}: {e}")
                continue
       
        print("No suitable icon file found for Calendar App. Using default icon.")
   
    def create_widgets(self):
        """Create and arrange GUI components for the calendar application"""
        # Main container frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
       
        # Left sidebar frame for calendar and controls
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
       
        # Calendar widget frame
        cal_frame = ttk.LabelFrame(left_frame, text="Calendar", padding="10")
        cal_frame.pack(fill=tk.X, pady=(0, 10))
       
        # Calendar widget with current date selection
        self.cal = Calendar(cal_frame, selectmode='day',
                          year=datetime.now().year,
                          month=datetime.now().month,
                          day=datetime.now().day,
                          date_pattern='y-mm-dd')
        self.cal.pack(pady=5)
        self.cal.bind("<<CalendarSelected>>", self.on_date_select)
       
        # Navigation buttons frame
        nav_frame = ttk.Frame(cal_frame)
        nav_frame.pack(fill=tk.X, pady=(10, 0))
       
        # Navigation buttons
        ttk.Button(nav_frame, text="Today",
                  command=self.go_to_today).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="Prev Week",
                  command=self.prev_week).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="Next Week",
                  command=self.next_week).pack(side=tk.LEFT)
       
        # Event operations frame
        event_ops_frame = ttk.LabelFrame(left_frame, text="Event Operations", padding="10")
        event_ops_frame.pack(fill=tk.X, pady=(0, 10))
       
        # Operation buttons
        ttk.Button(event_ops_frame, text="Add Sample Class",
                  command=self.add_sample_class).pack(fill=tk.X, pady=2)
        ttk.Button(event_ops_frame, text="Clear Day Events",
                  command=self.clear_day_events).pack(fill=tk.X, pady=2)
        ttk.Button(event_ops_frame, text="View Week Schedule",
                  command=self.show_week_view).pack(fill=tk.X, pady=2)
       
        # Statistics display frame
        stats_frame = ttk.LabelFrame(left_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X)
       
        # Statistics variable and label
        self.stats_var = tk.StringVar()
        self.stats_var.set("Events: 0 | This week: 0")
        ttk.Label(stats_frame, textvariable=self.stats_var).pack()
       
        # Right side frame for events display and editing
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
       
        # Date display frame
        date_display_frame = ttk.Frame(right_frame)
        date_display_frame.pack(fill=tk.X, pady=(0, 10))
       
        # Date label showing selected date
        self.date_label = ttk.Label(date_display_frame,
                                   text="Today's Events",
                                   font=("Arial", 14, "bold"))
        self.date_label.pack(side=tk.LEFT)
       
        # Events list display frame
        list_frame = ttk.LabelFrame(right_frame, text="Events", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
       
        # Treeview widget for events list with columns
        columns = ("time", "event", "duration")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
       
        # Configure column headings
        self.tree.heading("time", text="Time")
        self.tree.heading("event", text="Event")
        self.tree.heading("duration", text="Duration")
       
        # Configure column widths
        self.tree.column("time", width=100)
        self.tree.column("event", width=300)
        self.tree.column("duration", width=80)
       
        # Add vertical scrollbar to treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
       
        # Layout treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
       
        # Bind selection events to treeview
        self.tree.bind("<Double-1>", self.on_event_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_event_select)
       
        # Event editing frame
        edit_frame = ttk.LabelFrame(right_frame, text="Add/Edit Event", padding="10")
        edit_frame.pack(fill=tk.X, pady=(10, 0))
       
        # Time input frame
        time_frame = ttk.Frame(edit_frame)
        time_frame.pack(fill=tk.X, pady=(0, 10))
       
        # Start time input
        ttk.Label(time_frame, text="Start Time:").pack(side=tk.LEFT, padx=(0, 5))
        self.start_time_var = tk.StringVar(value="09:00")
        time_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=3,
                                  textvariable=self.start_time_var,
                                  format="%02.0f:00")
        time_spinbox.pack(side=tk.LEFT, padx=(0, 10))
       
        # Duration input
        ttk.Label(time_frame, text="Duration (hours):").pack(side=tk.LEFT, padx=(0, 5))
        self.duration_var = tk.StringVar(value="1")
        duration_spinbox = ttk.Spinbox(time_frame, from_=0.5, to=8, increment=0.5,
                                      width=5, textvariable=self.duration_var)
        duration_spinbox.pack(side=tk.LEFT)
       
        # Event description input
        ttk.Label(edit_frame, text="Event Description:").pack(anchor=tk.W)
        self.event_text = tk.Text(edit_frame, height=4, width=50)
        self.event_text.pack(fill=tk.X, pady=(5, 10))
       
        # Button frame for event operations
        button_frame = ttk.Frame(edit_frame)
        button_frame.pack(fill=tk.X)
       
        # Event operation buttons
        self.add_btn = ttk.Button(button_frame, text="Add Event",
                                 command=self.add_event)
        self.add_btn.pack(side=tk.LEFT, padx=(0, 10))
       
        self.update_btn = ttk.Button(button_frame, text="Update Event",
                                    command=self.update_event, state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT, padx=(0, 10))
       
        self.delete_btn = ttk.Button(button_frame, text="Delete Event",
                                    command=self.delete_event, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT)
       
        # Initialize button states
        self.selected_event_index = None
       
        # Update statistics display
        self.update_stats()
   
    def on_date_select(self, event):
        """Handle calendar date selection event"""
        selected_date = self.cal.get_date()
        self.current_date = selected_date
        self.show_date_events(selected_date)
   
    def show_date_events(self, date_str):
        """Display events for the specified date"""
        # Update date label with formatted date
        display_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A, %B %d, %Y")
        self.date_label.config(text=f"Events for {display_date}")
       
        # Clear existing items from treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
       
        # Display events for selected date if they exist
        if date_str in self.events:
            events = sorted(self.events[date_str], key=lambda x: x["start_time"])
            for event in events:
                self.tree.insert("", tk.END, values=(
                    event["start_time"],
                    event["description"],
                    f"{event['duration']}h"
                ))
       
        # Reset selection state
        self.selected_event_index = None
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.event_text.delete(1.0, tk.END)
   
    def on_event_select(self, event):
        """Handle event selection from treeview"""
        selected = self.tree.selection()
        if selected:
            self.selected_event_index = self.tree.index(selected[0])
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
           
            # Populate edit fields with selected event data
            date_events = self.events.get(self.current_date, [])
            if self.selected_event_index < len(date_events):
                event_data = date_events[self.selected_event_index]
                self.start_time_var.set(event_data["start_time"])
                self.duration_var.set(str(event_data["duration"]))
                self.event_text.delete(1.0, tk.END)
                self.event_text.insert(1.0, event_data["description"])
   
    def on_event_double_click(self, event):
        """Handle double-click event on events (edit action)"""
        self.on_event_select(event)
        if self.selected_event_index is not None:
            self.update_event()
   
    def add_event(self):
        """Add a new event with validation and persistence"""
        start_time = self.start_time_var.get()
        duration = self.duration_var.get()
        description = self.event_text.get(1.0, tk.END).strip()
       
        # Validate user input
        if not description:
            messagebox.showerror("Error", "Please enter event description!")
            return
       
        try:
            duration_val = float(duration)
            if duration_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration!")
            return
       
        # Validate time format
        if not self.validate_time(start_time):
            messagebox.showerror("Error", "Please enter a valid time (HH:MM)!")
            return
       
        # Create event dictionary
        event = {
            "start_time": start_time,
            "duration": duration_val,
            "description": description
        }
       
        # Use data manager to add event
        success = CalendarDataManager.add_event(self.current_date, event)
        if success:
            self.load_events() # Reload data from file
            self.show_date_events(self.current_date)
            self.update_stats()
            messagebox.showinfo("Success", "Event added successfully!")
        else:
            messagebox.showerror("Error", "Failed to save event!")
   
    def update_event(self):
        """Update selected event with new data"""
        if self.selected_event_index is not None:
            return
       
        start_time = self.start_time_var.get()
        duration = self.duration_var.get()
        description = self.event_text.get(1.0, tk.END).strip()
       
        # Validate user input
        if not description:
            messagebox.showerror("Error", "Please enter event description!")
            return
       
        try:
            duration_val = float(duration)
            if duration_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration!")
            return
       
        if not self.validate_time(start_time):
            messagebox.showerror("Error", "Please enter a valid time (HH:MM)!")
            return
       
        # Prepare update data
        update = {
            "start_time": start_time,
            "duration": duration_val,
            "description": description
        }

        # Use data manager to update event
        success = CalendarDataManager.update_event(
            self.current_date,
            self.selected_event_index,
            update
        )

        if success:
            self.load_events() # Reload data from file
            self.show_date_events(self.current_date)
            self.update_stats()
            messagebox.showinfo("Success", "Event updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update event!")
   
    def delete_event(self):
        """Delete selected event after confirmation"""
        if self.selected_event_index is None:
            return
       
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this event?"):
            # Use data manager to delete event
            success = CalendarDataManager.delete_event(
                self.current_date,
                self.selected_event_index
            )

            if success:
                self.load_events() # Reload data from file
                self.show_date_events(self.current_date)
                self.update_stats()
   
    def clear_day_events(self):
        """Clear all events for current date after confirmation"""
        if self.current_date in self.events:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete ALL events for this day?"):
                del self.events[self.current_date]
                self.save_events()
                self.show_date_events(self.current_date)
                self.update_stats()
   
    def add_sample_class(self):
        """Add sample class events for demonstration purposes"""
        sample_classes = [
            {"start_time": "09:00", "duration": 2, "description": "AMCS1034 - Software Development Lecture"},
            {"start_time": "11:00", "duration": 1, "description": "MATH101 - Calculus Tutorial"},
            {"start_time": "14:00", "duration": 3, "description": "Programming Lab Session"},
            {"start_time": "16:00", "duration": 1, "description": "Group Meeting for Assignment"}
        ]
       
        if self.current_date not in self.events:
            self.events[self.current_date] = []
       
        for cls in sample_classes:
            cls["created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.events[self.current_date].append(cls)
       
        self.save_events()
        self.show_date_events(self.current_date)
        self.update_stats()
        messagebox.showinfo("Info", "Sample classes added for today!")
   
    def show_week_view(self):
        """Display weekly schedule in a new window with navigation options"""
        week_win = tk.Toplevel(self)
        week_win.title("Weekly Schedule Viewer")
        week_win.geometry("900x700")
       
        # Set week view window icon
        try:
            icon_paths = ["icon.ico", "assets/icon.ico", "images/icon.ico"]
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    week_win.iconbitmap(icon_path)
                    break
        except:
            pass
       
        # Navigation frame for week selection
        nav_frame = ttk.Frame(week_win)
        nav_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
       
        # Store the current week start date for navigation
        current_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        current_week_start = current_week_start.replace(hour=0, minute=0, second=0, microsecond=0)
       
        # Function to display week schedule
        def display_week_schedule(week_start_date):
            # Clear previous content
            text_widget.delete(1.0, tk.END)
           
            # Update navigation label
            week_end_date = week_start_date + timedelta(days=6)
            nav_label.config(text=f"Week: {week_start_date.strftime('%Y-%m-%d')} to {week_end_date.strftime('%Y-%m-%d')}")
           
            text_widget.insert(tk.END, "=== WEEKLY SCHEDULE ===\n\n")
           
            # Display events for each day of the week
            for i in range(7):
                current_date = week_start_date + timedelta(days=i)
                date_str = current_date.strftime("%Y-%m-%d")
                display_date = current_date.strftime("%A, %B %d")
               
                text_widget.insert(tk.END, f"\n{display_date}:\n")
                text_widget.insert(tk.END, "-" * 60 + "\n")
               
                if date_str in self.events and self.events[date_str]:
                    events = sorted(self.events[date_str], key=lambda x: x["start_time"])
                    for event in events:
                        text_widget.insert(tk.END, f"{event['start_time']} - {event['description']} ({event['duration']}h)\n")
                else:
                    text_widget.insert(tk.END, "No events scheduled\n")
                text_widget.insert(tk.END, "\n")
       
        # Navigation buttons
        def go_prev_week():
            nonlocal current_week_start
            current_week_start -= timedelta(weeks=1)
            display_week_schedule(current_week_start)
       
        def go_next_week():
            nonlocal current_week_start
            current_week_start += timedelta(weeks=1)
            display_week_schedule(current_week_start)
       
        def go_current_week():
            nonlocal current_week_start
            current_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
            current_week_start = current_week_start.replace(hour=0, minute=0, second=0, microsecond=0)
            display_week_schedule(current_week_start)
       
        # Navigation buttons
        ttk.Button(nav_frame, text="← Previous Week", command=go_prev_week).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(nav_frame, text="Current Week", command=go_current_week).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(nav_frame, text="Next Week →", command=go_next_week).pack(side=tk.LEFT)
       
        # Week display label
        nav_label = ttk.Label(nav_frame, text="", font=("Arial", 10, "bold"))
        nav_label.pack(side=tk.RIGHT)
       
        # Create text widget for weekly schedule with scrollbar
        text_frame = ttk.Frame(week_win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
       
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
       
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
       
        # Display current week initially
        display_week_schedule(current_week_start)
       
        text_widget.config(state=tk.DISABLED)  # Set as read-only
       
        # Function to enable editing temporarily for navigation
        def enable_editing():
            text_widget.config(state=tk.NORMAL)
       
        # Re-disable after navigation
        def disable_editing():
            text_widget.config(state=tk.DISABLED)
       
        # Bind navigation functions to enable/disable editing
        original_prev_week = go_prev_week
        original_next_week = go_next_week
        original_current_week = go_current_week
       
        def wrapped_prev_week():
            enable_editing()
            original_prev_week()
            disable_editing()
       
        def wrapped_next_week():
            enable_editing()
            original_next_week()
            disable_editing()
       
        def wrapped_current_week():
            enable_editing()
            original_current_week()
            disable_editing()
       
        # Update button commands
        for widget in nav_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                if widget.cget("text") == "← Previous Week":
                    widget.config(command=wrapped_prev_week)
                elif widget.cget("text") == "Current Week":
                    widget.config(command=wrapped_current_week)
                elif widget.cget("text") == "Next Week →":
                    widget.config(command=wrapped_next_week)
   
    def go_to_today(self):
        """Navigate to today's date in calendar"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.cal.selection_set(today)
        self.current_date = today
        self.show_date_events(today)
   
    def prev_week(self):
        """Navigate to previous week"""
        current_date = datetime.strptime(self.current_date, "%Y-%m-%d")
        new_date = current_date - timedelta(weeks=1)
        new_date_str = new_date.strftime("%Y-%m-%d")
        self.cal.selection_set(new_date_str)
        self.current_date = new_date_str
        self.show_date_events(new_date_str)
   
    def next_week(self):
        """Navigate to next week"""
        current_date = datetime.strptime(self.current_date, "%Y-%m-%d")
        new_date = current_date + timedelta(weeks=1)
        new_date_str = new_date.strftime("%Y-%m-%d")
        self.cal.selection_set(new_date_str)
        self.current_date = new_date_str
        self.show_date_events(new_date_str)
   
    def validate_time(self, time_str):
        """Validate time string format (HH:MM)"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
   
    def update_stats(self):
        """Update statistics display with current event counts"""
        total_events = sum(len(events) for events in self.events.values())
       
        # Calculate events for current week
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        week_events = 0
       
        for i in range(7):
            date_str = (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d")
            if date_str in self.events:
                week_events += len(self.events[date_str])
       
        self.stats_var.set(f"Total Events: {total_events} | This Week: {week_events}")
   
    def load_events(self):
        """Load events from data manager"""
        self.events = CalendarDataManager.load_events()
   
    def save_events(self):
        """Save events using data manager"""
        CalendarDataManager.save_events(self.events)
   
    def on_close(self):
        """Cleanup operations when window is closed"""
        self.destroy()

# Test code for standalone execution
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main root window
    app = CalendarApp(root)
    app.mainloop()