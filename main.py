import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_session_data(year, grand_prix, session_type):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()
    return session

def load_driver_data(driver):
    lap = session.laps.pick_drivers(driver).pick_fastest()
    car_data = lap.get_car_data()
    time = car_data['Time']
    speed = car_data['Speed']
    style = fastf1.plotting.get_driver_style(identifier=driver, style=['color', 'linestyle'], session=session)
    data = {'Time': time, 'Speed': speed, 'Driver': driver}
    driver_colours.append(style)
    return data

def load_session_results(session):
    results = session.results
    return results[['DriverId', 'Abbreviation', 'TeamName', 'ClassifiedPosition', 'Points']]

def plot_data(dataframe, axes):
    for index, axis in enumerate(axes):
        driver_data = dataframe[dataframe['Driver'] == drivers[index]]
        axis.plot(driver_data['Time'], driver_data['Speed'], label=drivers[index], **driver_colours[index])
        axis.set_title(f'{drivers[index]} Speed during Monaco 2023 Race')
        axis.set_xlabel('Time (s)')
        axis.set_ylabel('Speed (km/h)')
        axis.legend()

if __name__ == "__main__":
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

    session = load_session_data(2023, 'Monaco', 'Race')
    results = load_session_results(session)
    print("\nSession Results:")
    print(results)

    drivers = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS']
    driver_colours = []
    dataframe = pd.DataFrame()

    for driver in drivers:
        dfs = [pd.DataFrame(load_driver_data(driver))]
        dataframe = pd.concat([dataframe, *dfs], ignore_index=True)

    print("\nDriver Data Loaded:")
    print(dataframe.columns.values)

    fig, ax = plt.subplots(3, 2, figsize=(16, 8))
    ax = ax.flatten()
    
    plot_data(dataframe, ax)
    plt.tight_layout()

    print("\nStatistical Summary:")
    for driver in drivers:
        print(f"Statistics for {driver}:")
        print(dataframe[dataframe['Driver'] == driver].describe())
        print("\n")

    plt.show()

