import json

class EventFileManager:
    FILE_PATH = "event.json"

    @classmethod
    def read_events_from_file(cls):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                events = json.load(file)
        except FileNotFoundError:
            events = []
        return events

    @classmethod
    def write_events_to_file(cls, events):
        with open(cls.FILE_PATH, "w") as file:
            json.dump(events, file)

