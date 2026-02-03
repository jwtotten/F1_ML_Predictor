from rich.table import Table
from rich.console import Console
import questionary

from utils import load_session_data, load_event_schedule, load_race_event, select_race_data, build_race_result_table_header
from methods import collect_all_race_info_by_season

class RaceDataAnalyzer:
    def __init__(self):
        self.drivers = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS']
        self.seasons = ['2022', '2023', '2024', '2025']
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
    
    def reset_view(func):
        def wrapper(self, *args, **kwargs):
            # clear the terminal
            print("\033c", end="")
            # Print the app name
            self.display_app_name()
            return func(self, *args, **kwargs)
        return wrapper
    
    @reset_view
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
    
    @reset_view
    def select_race(self):

        self.race_choice = questionary.select(
            "Select the race you want to analyze:",
            choices=self.event_names
        ).ask()
    
    @reset_view
    def present_tabulated_race_data(self):
        table = build_race_result_table_header(self.race_choice, self.season_choice)
        _race_data = select_race_data(self.race_data, self.race_choice)
        for driver, data in _race_data.items():
            position = str(data["Position"])
            points = str(data["Points"])
            table.add_row(driver, position, points)
        self.rich_console.print(table)

        restart = questionary.confirm("Would you like to analyze another race?").ask()
        return restart

    def _return_race_data(self):
        _race_data = select_race_data(self.race_data, self.race_choice)
        return _race_data