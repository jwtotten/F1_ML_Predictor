from rich.table import Table
from rich.console import Console
import asciichartpy as ac
import questionary
from typing import List, Dict, Any

from utils import (
    load_session_data,
    load_event_schedule,
    load_race_event,
    select_race_data,
    build_race_result_table_header,
)

SUPPORTED_DRIVERS = ["VER", "PER", "LEC", "SAI", "HAM", "RUS"]
SUPPORTED_SEASONS = ["2022", "2023", "2024", "2025"]


class RaceDataAnalyzer:
    def __init__(self):
        self.drivers = SUPPORTED_DRIVERS
        self.seasons = SUPPORTED_SEASONS
        self.rich_console = Console()

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

    @staticmethod
    def reset_view(func):
        def wrapper(self, *args, **kwargs):
            # clear the terminal
            print("\033c", end="")
            # Print the app name
            self.display_app_name()
            return func(self, *args, **kwargs)

        return wrapper

    @reset_view
    def select_season(self) -> str:
        self.season_choice = questionary.select(
            "Select the year for analysis:", choices=self.seasons
        ).ask()

        return self.season_choice

    def load_all_season_race_info(self) -> List[Dict[str, Any]]:
        event_schedule = load_event_schedule(int(self.season_choice))
        all_event_data = self.collect_all_race_info_by_season(event_schedule)
        return all_event_data

    def load_all_race_data(self, all_event_data: List[Dict[str, Any]]) -> List:
        self.race_data = []
        self.event_names = []
        for event in all_event_data:
            self.event_names.append(event["EventName"])
            self.race_data.append(
                {
                    event["EventName"]: load_race_event(
                        int(self.season_choice), event["EventName"]
                    )
                }
            )
        return self.race_data

    @reset_view
    def select_race(self) -> str:
        self.race_choice = questionary.select(
            "Select the race you want to analyze:", choices=self.event_names
        ).ask()

    def _get_selected_race_data(self):
        """Retrieve data for the currently selected race."""
        return select_race_data(self.race_data, self.race_choice)

    @reset_view
    def present_tabulated_race_data(self) -> str:
        table = build_race_result_table_header(self.race_choice, self.season_choice)
        _race_data = self._get_selected_race_data()
        for driver, data in _race_data.items():
            position = str(data["Position"])
            points = str(data["Points"])
            table.add_row(driver, position, points)
        self.rich_console.print(table)
        restart = questionary.confirm("Would you like to analyze another race?").ask()
        return restart

    def _return_race_data(self):
        return self._get_selected_race_data()

    @reset_view
    def plot_driver_season_results(self, data: List[list]) -> None:
        """
        Plot driver finishing positions throughout the season as an ASCII line graph.

        :param data: List of [race_number, finishing_position] pairs
        :type data: List[List[int, float]]
        """
        finishing_positions: List[float] = [result[1] for result in data]
        race_numbers = [result[0] for result in data]

        chart = ac.plot(
            finishing_positions,
            {
                "title": "Driver Finishing Positions Over the Season",
                "height": 10,
                "width": 80,  # Increased width to ensure x-axis labels fit
                "xAxis": race_numbers,
            },
        )
        print(chart + "\n\n")

    @staticmethod
    def collect_all_race_info_by_season(event_schedule):
        all_event_data = []
        for _, event in event_schedule.iterrows():
            event_name, round_number = event["EventName"], event["RoundNumber"]
            all_event_data.append(
                {"EventName": event_name, "RoundNumber": round_number}
            )
        return all_event_data

    def _season_results_for_driver(self, driver_code: str) -> List[Dict[str, Any]]:
        """
        Return a list of race results for a given driver across the selected season.

        :param driver_code: The three-letter code representing the driver (e.g., 'VER' for Max Verstappen).
        :type driver_code: str

        :return: A list of dictionaries containing the event name, position, and points for each race
        :rtype: List[Dict[str, Any]]
        """
        results = []
        for race_index, race in enumerate(self.race_data):
            for _, race_info in race.items():
                if driver_code in race_info:
                    results.append([race_index + 1, race_info[driver_code]["Position"]])
        return results

    def present_driver_season_results(self, driver_code: str) -> None:
        """
        Present the season results for a given driver in a tabulated format.

        :param driver_code: The three-letter code representing the driver (e.g., 'VER' for Max Verstappen).
        :type driver_code: str
        """
        table = Table(title=f"{self.season_choice} Season Results for {driver_code}")
        table.add_column("Race Number", justify="center")
        table.add_column("Position", justify="center")
        season_results = self._season_results_for_driver(driver_code)
        race_number = [i for i in range(1, len(season_results) + 1)]
        for i in range(len(season_results)):
            table.add_row(str(race_number[i]), str(season_results[i][1]))
        self.rich_console.print(table)
