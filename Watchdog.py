import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


#Define the function to run the external script when a new file is detected
def run_script(file_path = r"D:\alt\\"):
    print(f"New file detected: {file_path}")
    # Replace 'your_script.py' with the path to your script
    # Pass the file_path as an argument if needed
    try:
        subprocess.run(['streamlit', 'run', 'main.py', file_path])  # Modify as needed
        #subprocess.run(['python', r"D:\Battery\Main.py", file_path])
    except Exception as e:
        print(f"Error running script: {e}")

# Create a custom event handler
class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the created event is for a file
        if not event.is_directory:
            run_script(event.src_path)

# Function to start monitoring the folder
def monitor_folder(folder_path):
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_monitor = r"C:\Users\AIRSHOW\Downloads\Raw To Engineering Logs Converter\Engineering Logs\\"  # Replace with your folder path
    print(f"Monitoring folder: {folder_to_monitor}")
    monitor_folder(folder_to_monitor)
