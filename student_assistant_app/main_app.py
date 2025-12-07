# Import Tkinter module with alias `tk`
import tkinter as tk
from tkinter import ttk  # ttk provides modern themed widgets
from reminder_app import ReminderApp
from calendar_app import CalendarApp
import os

# Main application window class
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize parent class (tk.Tk)
        
        # Configure main window properties
        self.title("TARUMT Student Assistant")  # Window title
        self.geometry("700x500")  # Set window size (width x height)
        self.configure(bg='#f0f0f0')  # Set background color
        
        # Set window icon - try multiple approaches
        self.set_window_icon()
        
        # Configure custom styles for widgets
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f0f8ff")  # Frame background
        self.style.configure('TLabel', background='#f0f8ff')  # Label background
        self.style.configure('Title.TLabel', font=('Arial', 20, 'bold'), foreground="#000000")  # Title style
        self.style.configure('Subtitle.TLabel', font=('Arial', 12), foreground="#000000")  # Subtitle style
        self.style.configure('Big.TButton', font=('Arial', 12), padding=(30, 15))  # Large button style
        
        # Create main container frame with padding
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)  # Expand to fill available space
        
        # Create and pack title label
        title_label = ttk.Label(
            main_frame, 
            text="TARUMT Student Assistant", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))  # Add vertical padding (top, bottom)
        
        # Create and pack subtitle label
        subtitle_label = ttk.Label(
            main_frame,
            text="Manage your schedule and reminders efficiently",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(pady=(0, 50))  # Add vertical padding
        
        # Create frame for buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)  # Add vertical padding around button frame
        
        # Create reminder application button
        reminder_btn = ttk.Button(
            button_frame,
            text="Open Reminder App",
            command=self.show_reminder_page,  # Set button click handler
            style='Big.TButton'
        )
        reminder_btn.pack(pady=15, fill=tk.X)  # Fill horizontally, add padding
        
        # Create calendar application button
        calendar_btn = ttk.Button(
            button_frame,
            text="Open Calendar App", 
            command=self.show_calendar_page,  # Set button click handler
            style='Big.TButton'
        )
        calendar_btn.pack(pady=15, fill=tk.X)  # Fill horizontally, add padding
        
        # Create footer frame for version information
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(side=tk.BOTTOM, pady=20)  # Position at bottom with padding
        
        # Create version information label
        version_label = ttk.Label(
            info_frame,
            text="Version 1.0 - 2025",
            style='Subtitle.TLabel'
        )
        version_label.pack()
        
        # Center the window on screen
        self.center_window()
    
    def set_window_icon(self):
        """Set window icon with multiple fallback options"""
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
                        print(f"Icon set from: {icon_path}")
                        return
                    elif icon_path.endswith(('.png', '.jpg', '.gif')):
                        # For image files, use iconphoto
                        from PIL import Image, ImageTk
                        icon_image = Image.open(icon_path)
                        icon_photo = ImageTk.PhotoImage(icon_image)
                        self.iconphoto(False, icon_photo)
                        print(f"Icon set from: {icon_path}")
                        return
            except Exception as e:
                print(f"Error loading icon {icon_path}: {e}")
                continue
        
        print("No suitable icon file found. Using default icon.")
    
    def center_window(self):
        """Center the main window on the screen"""
        self.update_idletasks()  # Update widget geometry information
        width = self.winfo_width()  # Get current window width
        height = self.winfo_height()  # Get current window height
        x = (self.winfo_screenwidth() // 2) - (width // 2)  # Calculate x position
        y = (self.winfo_screenheight() // 2) - (height // 2)  # Calculate y position
        self.geometry(f'{width}x{height}+{x}+{y}')  # Set window position
    
    def show_reminder_page(self):
        """Open the Reminder application window"""
        try:
            reminder_window = ReminderApp(self)  # Create ReminderApp instance
            reminder_window.grab_set()  # Make window modal (focus grab)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Cannot open Reminder: {e}")  # Show error message
    
    def show_calendar_page(self):
        """Open the Calendar application window"""
        try:
            calendar_window = CalendarApp(self)  # Create CalendarApp instance
            calendar_window.grab_set()  # Make window modal (focus grab)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Cannot open Calendar: {e}")  # Show error message

# Entry point check - only run if this file is executed directly
if __name__ == "__main__":
    app = MainApplication()  # Create application instance
    app.mainloop()  # Start the GUI event loop (blocks until window closes)