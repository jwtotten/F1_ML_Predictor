from rich.table import Table

def build_race_result_table_header(race_choice: str, season_choice: str) -> Table:
    table = Table(title=f"Race Data for {race_choice} - {season_choice} Season")
    table.add_column("Driver", justify="center", style="cyan", no_wrap=True)
    table.add_column("Position", justify="center", style="magenta")
    table.add_column("Points", justify="center", style="green")
    return table

