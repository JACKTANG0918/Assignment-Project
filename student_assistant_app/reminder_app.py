import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import time
import threading
from data_manager import ReminderDataManager

class ReminderApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Simple Reminder App")
        self.geometry("800x500")
        self.resizable(True, True)
        
        # Set background color
        self.configure(bg='#f0f8ff')
        
        # Set window icon (using the same icon as main_app)
        self.set_window_icon()
        
        # Initialize reminders data storage
        self.reminders = []
        self.data_file = "reminders.json"
        
        # Load existing reminders from storage
        self.load_reminders()
        
        # Create and setup GUI components
        self.create_widgets()
        
        # Start background thread for checking reminders
        self.running = True
        self.check_thread = threading.Thread(target=self.check_reminders_background, daemon=True)
        self.check_thread.start()
        
        # Bind window close event handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
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
                        print(f"Reminder App icon set from: {icon_path}")
                        return
                    elif icon_path.endswith(('.png', '.jpg', '.gif')):
                        # For image files, use iconphoto
                        from PIL import Image, ImageTk
                        icon_image = Image.open(icon_path)
                        icon_photo = ImageTk.PhotoImage(icon_image)
                        self.iconphoto(False, icon_photo)
                        print(f"Reminder App icon set from: {icon_path}")
                        return
            except Exception as e:
                print(f"Error loading icon {icon_path}: {e}")
                continue
        
        print("No suitable icon file found for Reminder App. Using default icon.")
    
    def create_widgets(self):
        """Create and arrange GUI components for the reminder application"""
        # Main container frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Manually set main frame background color
        style = ttk.Style()
        style.configure('Main.TFrame', background='#f0f8ff')
        style.configure('TLabel', background='#f0f8ff', foreground='#2c3e50')
        style.configure('TLabelframe', background='#f0f8ff')
        style.configure('TLabelframe.Label', background='#f0f8ff', foreground='#2c3e50')
        
        # Input section frame with label
        input_frame = ttk.LabelFrame(main_frame, text="Add New Reminder", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Configure input frame background color
        style.configure('Input.TLabelframe', background='#f0f8ff')
        style.configure('Input.TLabelframe.Label', background='#f0f8ff', foreground='#2c3e50')
        input_frame.configure(style='Input.TLabelframe')
        
        # Reminder content label and entry field
        ttk.Label(input_frame, text="Reminder Content:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.content_entry = ttk.Entry(input_frame, width=40)
        self.content_entry.grid(row=0, column=1, padx=(0, 10))
        self.content_entry.bind("<Return>", lambda e: self.add_reminder())  # Bind Enter key to add reminder
        
        # Date input label and entry field
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.date_entry = ttk.Entry(input_frame, width=12)
        self.date_entry.grid(row=0, column=3, padx=(0, 10))
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Set default to current date
        
        # Time input label and entry field
        ttk.Label(input_frame, text="Time (HH:MM):").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.time_entry = ttk.Entry(input_frame, width=8)
        self.time_entry.grid(row=0, column=5, padx=(0, 10))
        self.time_entry.insert(0, "12:00")  # Set default time
        
        # Add reminder button
        add_btn = ttk.Button(input_frame, text="Add Reminder", command=self.add_reminder)
        add_btn.grid(row=0, column=6, padx=(10, 0))
        
        # List display frame for scheduled reminders
        list_frame = ttk.LabelFrame(main_frame, text="Scheduled Reminders", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure list frame background color
        style.configure('List.TLabelframe', background='#e6f2ff')
        style.configure('List.TLabelframe.Label', background='#e6f2ff', foreground='#2c3e50')
        list_frame.configure(style='List.TLabelframe')
        
        # Create Treeview widget with scrollbar for reminder list
        columns = ("content", "date", "time", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure column headings
        self.tree.heading("content", text="Content")
        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("status", text="Status")
        
        # Configure column widths
        self.tree.column("content", width=300)
        self.tree.column("date", width=100)
        self.tree.column("time", width=80)
        self.tree.column("status", width=100)
        
        # Configure Treeview style
        style.configure('Treeview', 
                       background='white', 
                       foreground='#2c3e50',
                       fieldbackground='white')
        
        style.configure('Treeview.Heading', 
                       background='#4a86e8', 
                       foreground='white',
                       font=('Arial', 9, 'bold'))
        
        # Add vertical scrollbar to the treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event to treeview items
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # Button frame for operations
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Configure button frame background color
        style.configure('Button.TFrame', background='#f0f8ff')
        button_frame.configure(style='Button.TFrame')
        
        # Delete selected reminder button
        delete_btn = ttk.Button(button_frame, text="Delete Selected", command=self.delete_reminder)
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear all reminders button
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all_reminders)
        clear_btn.pack(side=tk.LEFT)
        
        # Status bar at bottom to show reminder count
        self.status_var = tk.StringVar()
        self.status_var.set(f"Total reminders: {len(self.reminders)}")
        
        # Use standard Label instead of ttk Label to set background color
        status_bar = tk.Label(self, 
                            textvariable=self.status_var, 
                            relief=tk.SUNKEN,
                            bg='#4a86e8',
                            fg='white',
                            font=('Arial', 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Refresh the reminder list display
        self.refresh_list()
    
    def add_reminder(self):
        """Add a new reminder with validation and user feedback"""
        content = self.content_entry.get().strip()
        date_str = self.date_entry.get().strip()
        time_str = self.time_entry.get().strip()
        
        # Validate user input
        if not content:
            messagebox.showerror("Error", "Please enter reminder content!")
            return
        
        if not self.validate_date(date_str):
            messagebox.showerror("Error", "Please enter a valid date (YYYY-MM-DD)!")
            return
        
        if not self.validate_time(time_str):
            messagebox.showerror("Error", "Please enter a valid time (HH:MM)!")
            return
        
        # Create reminder dictionary with metadata
        reminder = {
            "content": content,
            "date": date_str,
            "time": time_str,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "triggered": False
        }
        
        # Add to list and persist to storage
        self.reminders.append(reminder)
        self.save_reminders()
        self.refresh_list()
        
        # Clear input fields and reset time default
        self.content_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "12:00")  # Reset to default time
        
        # Show success message
        messagebox.showinfo("Success", "Reminder added successfully!")
    
    def validate_date(self, date_str):
        """Validate date string format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def validate_time(self, time_str):
        """Validate time string format (HH:MM)"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    def delete_reminder(self):
        """Delete selected reminder after confirmation"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reminder to delete!")
            return
        
        # Confirm deletion with user
        if messagebox.askyesno("Confirm", "Are you sure you want to delete the selected reminder?"):
            for item in selected:
                index = self.tree.index(item)
                if 0 <= index < len(self.reminders):
                    del self.reminders[index]
            
            # Save changes and refresh display
            self.save_reminders()
            self.refresh_list()
    
    def clear_all_reminders(self):
        """Clear all reminders after confirmation"""
        if not self.reminders:
            return
        
        # Confirm complete clearance with user
        if messagebox.askyesno("Confirm", "Are you sure you want to delete ALL reminders?"):
            self.reminders.clear()
            self.save_reminders()
            self.refresh_list()
    
    def on_item_double_click(self, event):
        """Handle double-click event on reminder items (delete action)"""
        selected = self.tree.selection()
        if selected:
            self.delete_reminder()
    
    def refresh_list(self):
        """Refresh the reminder list display with current data"""
        # Clear existing items from treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Sort reminders by date and time
        sorted_reminders = sorted(self.reminders, key=lambda x: (x["date"], x["time"]))
        
        # Add sorted reminders to treeview
        for reminder in sorted_reminders:
            status = "Pending"
            if reminder.get("triggered"):
                status = "Triggered"
            
            self.tree.insert("", tk.END, values=(
                reminder["content"],
                reminder["date"],
                reminder["time"],
                status
            ))
        
        # Update status bar with current counts
        pending_count = len([r for r in self.reminders if not r.get('triggered')])
        status_text = f"Total reminders: {len(self.reminders)} | Pending: {pending_count}"
        self.status_var.set(status_text)
    
    def check_reminders_background(self):
        """Background thread function to check for due reminders"""
        while self.running:
            try:
                current_time = datetime.now()
                current_date = current_time.strftime("%Y-%m-%d")
                current_time_str = current_time.strftime("%H:%M")
                
                # Check each reminder for trigger condition
                for reminder in self.reminders:
                    if (not reminder.get("triggered") and 
                        reminder["date"] == current_date and 
                        reminder["time"] == current_time_str):
                        
                        # Mark reminder as triggered and save
                        reminder["triggered"] = True
                        self.save_reminders()
                        
                        # Show notification in main thread
                        self.after(0, self.show_notification, reminder["content"])
                
                # Check every 30 seconds
                time.sleep(30)
                
            except Exception as e:
                print(f"Error in reminder check: {e}")
                time.sleep(60)  # Longer delay on error
    
    def show_notification(self, content):
        """Display notification window for triggered reminder"""
        # Create notification window
        notify_win = tk.Toplevel(self)
        notify_win.title("Reminder!")
        notify_win.geometry("400x200")
        notify_win.resizable(False, False)
        
        # Set notification window background color
        notify_win.configure(bg='#f0f8ff')
        
        # Set notification window icon (same as main window)
        try:
            icon_paths = ["icon.ico", "assets/icon.ico", "images/icon.ico"]
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    notify_win.iconbitmap(icon_path)
                    break
        except:
            pass
        
        # Set window properties
        notify_win.transient(self)  # Set as transient to main window
        notify_win.grab_set()  # Grab focus
        
        # Notification content labels
        label1 = tk.Label(notify_win, text="⏰ REMINDER ⏰", 
                         font=("Arial", 16, "bold"),
                         bg='#f0f8ff', fg='#e74c3c')
        label1.pack(pady=20)
        
        label2 = tk.Label(notify_win, text=content, 
                         font=("Arial", 12), 
                         wraplength=350,
                         bg='#f0f8ff', fg='#2c3e50')
        label2.pack(pady=10)
        
        # Confirmation button
        ok_btn = tk.Button(notify_win, text="OK", 
                          command=notify_win.destroy,
                          bg='#4a86e8', fg='white',
                          font=("Arial", 10))
        ok_btn.pack(pady=20)
        
        # Refresh list to show updated status
        self.refresh_list()
        
        # Force focus to notification window
        notify_win.focus_force()
    
    def load_reminders(self):
        """Load reminders from data manager"""
        self.reminders = ReminderDataManager.load_reminders()
    
    def save_reminders(self):
        """Save reminders using data manager"""
        ReminderDataManager.save_reminders(self.reminders)
    
    def on_close(self):
        """Cleanup operations when window is closed"""
        self.running = False  # Stop background thread
        if self.check_thread.is_alive():
            self.check_thread.join(timeout=1.0)  # Wait for thread to finish
        self.destroy()  # Close window

# Test code for standalone execution
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main root window
    app = ReminderApp(root)
    app.mainloop()