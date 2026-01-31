import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import questionary
import logging

from utils import load_session_data, load_event_schedule, load_race_event
from methods import collect_all_race_info_by_season

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RaceDataAnalyzer:
    def __init__(self):
        self.drivers = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS']
        self.seasons = ['2022', '2023', '2024', '2025']

    def display_app_name(self):
        
        welcome_message = """

        ███████╗ ██╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗██████╗ 
        ██╔════╝███║    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝██╔════╝██╔══██╗
        █████╗  ╚██║    ███████║██╔██╗ ██║███████║██║   ╚████╔╝ ███████╗█████╗  ██████╔╝
        ██╔══╝   ██║    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ╚════██║██╔══╝  ██╔══██╗
        ██║      ██║    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║███████╗██║  ██║
        ╚═╝      ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
                                                                                        
        """

        print(welcome_message)
    
    def select_season(self):       

        self.season_choice = questionary.select(
            "Select the year for analysis:",
            choices=self.seasons
        ).ask()

        return self.season_choice
    
    def load_all_season_race_info(self):
        event_schedule = load_event_schedule(int(self.season_choice))
        all_event_data = collect_all_race_info_by_season(event_schedule)
        return all_event_data

    def load_all_race_data(self, all_event_data: list[dict]):
        self.race_data = []
        self.event_names = []
        for event in all_event_data:
            self.event_names.append(event["EventName"])
            self.race_data.append({event["EventName"]: load_race_event(int(self.season_choice), event["EventName"])})
        return self.race_data
    
    def select_race(self):

        self.race_choice = questionary.select(
            "Select the race you want to analyze:",
            choices=self.event_names
        ).ask()


if __name__ == "__main__":
    
    race_analyzer = RaceDataAnalyzer()
    race_analyzer.display_app_name()
    season_choice = race_analyzer.select_season()
    all_race_event_data = race_analyzer.load_all_season_race_info()
    logger.info(f"Loaded data for {race_analyzer.season_choice} season:")
    for events in all_race_event_data[:5]: 
        logger.info(f"Round {events.get('RoundNumber')}: {events.get('EventName')}")
    all_race_data = race_analyzer.load_all_race_data(all_race_event_data)

    logger.info("Race data loading complete.")
    race_choice = race_analyzer.select_race()
