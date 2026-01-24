import fastf1

def load_event_schedule(year: int):
    return fastf1.get_event_schedule(year, include_testing=False)

def load_race_event(year, event_name: str):
    race = fastf1.get_event(year, event_name, 'R')
    race.load(laps=False, telemetry=False, weather=False, messages=False)
    return race

def load_session_data(year, grand_prix, session_type):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()
    return session