from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    events = EventFileManager.read_events_from_file()
    return events


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    events = EventFileManager.read_events_from_file()
    filtered_events = []
    for event_dict in events:
        event = Event(**event_dict)  # Convert dictionary to Event instance
        
        if (date is None or event.date == date) and \
           (organizer is None or event.organizer.name == organizer) and \
           (status is None or event.status == status) and \
           (event_type is None or event.type == event_type):
            filtered_events.append(event)

    return filtered_events


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    events = EventFileManager.read_events_from_file()

    for event_dict in events:
        if event_dict.get("id") == event_id:
            return Event(**event_dict)
        
    raise HTTPException(status_code=404, detail="Event not found")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    events = EventFileManager.read_events_from_file()
    for existed_event in events:
        if existed_event.get("id") == event.id:
            raise HTTPException(status_code=400, detail="Event ID already exist")
        
    events.append(event.dict())
    EventFileManager.write_events_to_file(events)
    
    return event


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event_data: Event):
    events = EventFileManager.read_events_from_file()

    event_index = None
    for i, event in enumerate(events):
        if event.get("id") == event_id:
            event_index = i
            break

    if event_index is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event_data.id = events[event_index].get("id")
    events[event_index] = event_data.dict()
    EventFileManager.write_events_to_file(events)
    
    return event_data


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    events = EventFileManager.read_events_from_file()

    index_event = None
    for i, event in enumerate(events):
        if event.get("id") == event_id:
            index_event = i
            break
    
    if index_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    del events[index_event]

    EventFileManager.write_events_to_file(events)
    return {"message": "Event deleted successfully"}



@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    events = EventFileManager.read_events_from_file()
    event_analyzer = EventAnalyzer()

    joiners_multiple_meetings = event_analyzer.get_joiners_multiple_meetings_method(events)

    if not joiners_multiple_meetings:
        return {"message": "No joiners attending at least 2 meetings"}
    
    return {"Joiners that attend multiple meetings": joiners_multiple_meetings}


