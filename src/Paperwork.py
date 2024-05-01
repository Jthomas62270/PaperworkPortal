import time
import os
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from CueList import extract_cue
from PatchList import extract_patch

API_URL = "http://127.0.0.1:5000/api/post"

class Watcher: 
    DIRECTORY_TO_WATCH = "./CUE_LISTS"

    def __init__(self):
        self.observer = Observer()

    def run(self): 
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try: 
            while True: 
                time.sleep(5)
        except: 
            self.observer.stop()
            print("Observer Stopped")
        
        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event): 
        if event.is_directory: 
            return None
        elif event.event_type == "created":
            print(f"Recived created event - {event.src_path}.")
            filename = os.path.basename(event.src_path)
            extract_data(filename)


def extract_data(path): 
    try: 
        extract_cue(path)
        # extract_patch(path)

        send_to_API(path)
    except: 
        print("Error: Cannot extract data...")

def send_to_API(path): 
    try: 
        show_url = API_URL + f"/shows/{path}"
        response = requests.get(show_url)
        print(response)

        cues_url = API_URL + f"/cues/{path}"
        response = requests.get(cues_url)
        print(response)
        
    except: 
        print("Error: Cannot access API... ")
