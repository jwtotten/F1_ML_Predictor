import fastf1

def load_event_schedule(year: int):
    return fastf1.events.EventSchedule(year)

def load_session_data(year, grand_prix, session_type):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()
    return session