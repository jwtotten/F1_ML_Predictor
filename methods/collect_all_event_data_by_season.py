import fastf1

def collect_all_race_info_by_season(event_schedule):
    all_event_data = []
    for _, event in event_schedule.iterrows():
        event_name, round_number = event["EventName"], event["RoundNumber"]
        all_event_data.append({
            "EventName": event_name,
            "RoundNumber": round_number
            })
    return all_event_data