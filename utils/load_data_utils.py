import fastf1

def load_event_schedule(year: int):
    return fastf1.get_event_schedule(year, include_testing=False)

def load_race_event(year, event_name: str):
    race = fastf1.get_session(year, event_name, 'R')
    race.load(laps=False, telemetry=False, weather=False, messages=False)
    race_data = {}
    for _, driver_row in race.results.iterrows():
        abbreviation, race_points, race_position = (
            driver_row["Abbreviation"],
            driver_row["Points"],
            driver_row["Position"],
        )
        race_data[abbreviation] = {"Points": race_points, "Position": race_position}
    return race_data

def load_session_data(year, grand_prix, session_type):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()
    return session