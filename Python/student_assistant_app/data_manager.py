# data_manager.py
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define data file paths
REMINDER_FILE = "data/reminders.json"
CALENDAR_FILE = "data/calendar_events.json"
USER_FILE = "data/user_settings.json"

# Ensure data directory exists
def ensure_data_directory():
    """Ensure the data directory exists"""
    data_dir = os.path.dirname(REMINDER_FILE)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info(f"Created data directory: {data_dir}")

# Reminder application data management
class ReminderDataManager:
    @staticmethod
    def load_reminders():
        """
        Load reminder data from file
        Returns: List of reminders
        """
        ensure_data_directory()
        try:
            if os.path.exists(REMINDER_FILE):
                with open(REMINDER_FILE, 'r', encoding='utf-8') as f:
                    reminders = json.load(f)
                    logger.info(f"Loaded {len(reminders)} reminders from {REMINDER_FILE}")
                    return reminders
            else:
                logger.info("No reminders file found, returning empty list")
                return []
        except Exception as e:
            logger.error(f"Error loading reminders: {e}")
            return []

    @staticmethod
    def save_reminders(reminders):
        """
        Save reminder data to file
        reminders: List of reminders to save
        """
        ensure_data_directory()
        try:
            with open(REMINDER_FILE, 'w', encoding='utf-8') as f:
                json.dump(reminders, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(reminders)} reminders to {REMINDER_FILE}")
            return True
        except Exception as e:
            logger.error(f"Error saving reminders: {e}")
            return False

    @staticmethod
    def add_reminder(reminder_data):
        """
        Add a new reminder
        reminder_data: Dictionary containing reminder data
        Returns: Boolean indicating success
        """
        reminders = ReminderDataManager.load_reminders()
        reminder_data["id"] = len(reminders) + 1
        reminder_data["created_at"] = datetime.now().isoformat()
        reminder_data["updated_at"] = datetime.now().isoformat()
        reminder_data["triggered"] = False
        
        reminders.append(reminder_data)
        return ReminderDataManager.save_reminders(reminders)

    @staticmethod
    def update_reminder(reminder_id, updates):
        """
        Update an existing reminder
        reminder_id: ID of the reminder to update
        updates: Dictionary of fields to update
        Returns: Boolean indicating success
        """
        reminders = ReminderDataManager.load_reminders()
        for reminder in reminders:
            if reminder.get("id") == reminder_id:
                reminder.update(updates)
                reminder["updated_at"] = datetime.now().isoformat()
                return ReminderDataManager.save_reminders(reminders)
        return False

    @staticmethod
    def delete_reminder(reminder_id):
        """
        Delete a reminder
        reminder_id: ID of the reminder to delete
        Returns: Boolean indicating success
        """
        reminders = ReminderDataManager.load_reminders()
        reminders = [r for r in reminders if r.get("id") != reminder_id]
        return ReminderDataManager.save_reminders(reminders)

    @staticmethod
    def get_reminder(reminder_id):
        """
        Get a specific reminder
        reminder_id: ID of the reminder to retrieve
        Returns: Reminder data or None if not found
        """
        reminders = ReminderDataManager.load_reminders()
        for reminder in reminders:
            if reminder.get("id") == reminder_id:
                return reminder
        return None

    @staticmethod
    def get_pending_reminders():
        """
        Get all reminders that haven't been triggered
        Returns: List of pending reminders
        """
        reminders = ReminderDataManager.load_reminders()
        return [r for r in reminders if not r.get("triggered", False)]

    @staticmethod
    def mark_reminder_triggered(reminder_id):
        """
        Mark a reminder as triggered
        reminder_id: ID of the reminder to mark
        Returns: Boolean indicating success
        """
        return ReminderDataManager.update_reminder(reminder_id, {"triggered": True})

# Calendar application data management
class CalendarDataManager:
    @staticmethod
    def load_events():
        """
        Load calendar events from file
        Returns: Dictionary of events {date: [events]}
        """
        ensure_data_directory()
        try:
            if os.path.exists(CALENDAR_FILE):
                with open(CALENDAR_FILE, 'r', encoding='utf-8') as f:
                    events = json.load(f)
                    logger.info(f"Loaded events for {len(events)} dates from {CALENDAR_FILE}")
                    return events
            else:
                logger.info("No calendar events file found, returning empty dict")
                return {}
        except Exception as e:
            logger.error(f"Error loading calendar events: {e}")
            return {}

    @staticmethod
    def save_events(events):
        """
        Save calendar events to file
        events: Dictionary of events to save
        """
        ensure_data_directory()
        try:
            with open(CALENDAR_FILE, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved events for {len(events)} dates to {CALENDAR_FILE}")
            return True
        except Exception as e:
            logger.error(f"Error saving calendar events: {e}")
            return False

    @staticmethod
    def add_event(date, event_data):
        """
        Add an event for a specific date
        date: Date string (YYYY-MM-DD)
        event_data: Dictionary containing event data
        Returns: Boolean indicating success
        """
        events = CalendarDataManager.load_events()
        
        if date not in events:
            events[date] = []
        
        event_data["id"] = len(events[date]) + 1
        event_data["created_at"] = datetime.now().isoformat()
        event_data["updated_at"] = datetime.now().isoformat()
        
        events[date].append(event_data)
        return CalendarDataManager.save_events(events)

    @staticmethod
    def update_event(date, event_index, updates):
        """
        Update an event for a specific date
        date: Date string
        event_index: Index of the event in the list
        updates: Dictionary of fields to update
        Returns: Boolean indicating success
        """
        events = CalendarDataManager.load_events()
        
        if date in events and event_index < len(events[date]):
            events[date][event_index].update(updates)
            events[date][event_index]["updated_at"] = datetime.now().isoformat()
            return CalendarDataManager.save_events(events)
        
        return False

    @staticmethod
    def delete_event(date, event_index):
        """
        Delete an event for a specific date
        date: Date string
        event_index: Index of the event in the list
        Returns: Boolean indicating success
        """
        events = CalendarDataManager.load_events()
        
        if date in events and event_index < len(events[date]):
            del events[date][event_index]
            
            # Remove date key if no events remain
            if not events[date]:
                del events[date]
                
            return CalendarDataManager.save_events(events)
        
        return False

    @staticmethod
    def get_events_for_date(date):
        """
        Get all events for a specific date
        date: Date string
        Returns: List of events
        """
        events = CalendarDataManager.load_events()
        return events.get(date, [])

    @staticmethod
    def get_events_for_week(start_date):
        """
        Get events for a week
        start_date: Start date of the week
        Returns: Dictionary of week events
        """
        from datetime import timedelta
        
        events = CalendarDataManager.load_events()
        week_events = {}
        
        for i in range(7):
            current_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
            if current_date in events:
                week_events[current_date] = events[current_date]
        
        return week_events

    @staticmethod
    def get_all_dates_with_events():
        """
        Get all dates that have events
        Returns: List of dates
        """
        events = CalendarDataManager.load_events()
        return list(events.keys())

# User settings management
class UserSettingsManager:
    @staticmethod
    def load_settings():
        """
        Load user settings
        Returns: Settings dictionary
        """
        ensure_data_directory()
        try:
            if os.path.exists(USER_FILE):
                with open(USER_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    logger.info("Loaded user settings")
                    return settings
            else:
                logger.info("No user settings file found, returning default settings")
                return UserSettingsManager.get_default_settings()
        except Exception as e:
            logger.error(f"Error loading user settings: {e}")
            return UserSettingsManager.get_default_settings()

    @staticmethod
    def save_settings(settings):
        """
        Save user settings
        settings: Settings dictionary to save
        Returns: Boolean indicating success
        """
        ensure_data_directory()
        try:
            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            logger.info("Saved user settings")
            return True
        except Exception as e:
            logger.error(f"Error saving user settings: {e}")
            return False

    @staticmethod
    def get_default_settings():
        """
        Get default user settings
        Returns: Default settings dictionary
        """
        return {
            "reminder": {
                "check_interval": 30,  # Check interval in seconds
                "notification_sound": True,
                "auto_start": False
            },
            "calendar": {
                "week_start": "monday",  # Week start day
                "time_format": "24h",    # Time format
                "default_view": "month"  # Default view
            },
            "app": {
                "theme": "light",
                "language": "en",
                "auto_save": True,
                "backup_interval": 3600  # Backup interval in seconds
            }
        }

    @staticmethod
    def update_setting(category, key, value):
        """
        Update a specific setting
        category: Setting category
        key: Setting key
        value: Setting value
        Returns: Boolean indicating success
        """
        settings = UserSettingsManager.load_settings()
        
        if category in settings and key in settings[category]:
            settings[category][key] = value
            return UserSettingsManager.save_settings(settings)
        
        return False

# Backup and utility functions
class BackupManager:
    @staticmethod
    def create_backup():
        """
        Create a data backup
        Returns: Backup file path
        """
        ensure_data_directory()
        try:
            backup_data = {
                "reminders": ReminderDataManager.load_reminders(),
                "calendar_events": CalendarDataManager.load_events(),
                "user_settings": UserSettingsManager.load_settings(),
                "backup_time": datetime.now().isoformat()
            }
            
            backup_file = f"data/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Created backup: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

    @staticmethod
    def restore_backup(backup_file):
        """
        Restore data from backup
        backup_file: Path to backup file
        Returns: Boolean indicating success
        """
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Restore data
            ReminderDataManager.save_reminders(backup_data.get("reminders", []))
            CalendarDataManager.save_events(backup_data.get("calendar_events", {}))
            UserSettingsManager.save_settings(backup_data.get("user_settings", {}))
            
            logger.info(f"Restored from backup: {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False

    @staticmethod
    def get_backup_files():
        """
        Get all backup files
        Returns: List of backup files
        """
        if not os.path.exists("data"):
            return []
        
        backup_files = [f for f in os.listdir("data") if f.startswith("backup_") and f.endswith(".json")]
        return sorted(backup_files, reverse=True)

# Data validation functions
class DataValidator:
    @staticmethod
    def validate_reminder_data(data):
        """Validate reminder data"""
        required_fields = ["content", "date", "time"]
        return all(field in data for field in required_fields)

    @staticmethod
    def validate_calendar_event_data(data):
        """Validate calendar event data"""
        required_fields = ["start_time", "duration", "description"]
        return all(field in data for field in required_fields)

    @staticmethod
    def validate_date(date_str):
        """Validate date format"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_time(time_str):
        """Validate time format"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

# Initialize data directory
ensure_data_directory()

# Test code
if __name__ == "__main__":
    # Test data manager
    print("Testing Data Manager...")
    
    # Test reminder data management
    test_reminder = {
        "content": "Test Reminder",
        "date": "2025-09-01",
        "time": "14:30"
    }
    
    if ReminderDataManager.add_reminder(test_reminder):
        print("✓ Reminder added successfully")
    
    reminders = ReminderDataManager.load_reminders()
    print(f"✓ Loaded {len(reminders)} reminders")
    
    # Test calendar data management
    test_event = {
        "start_time": "10:00",
        "duration": 2,
        "description": "Test Event"
    }
    
    if CalendarDataManager.add_event("2025-09-01", test_event):
        print("✓ Calendar event added successfully")
    
    # Test user settings
    settings = UserSettingsManager.load_settings()
    print(f"✓ Loaded user settings: {settings['app']['theme']}")
    
    # Create backup
    backup_file = BackupManager.create_backup()
    if backup_file:
        print(f"✓ Backup created: {backup_file}")
    
    print("Data manager test completed successfully!")