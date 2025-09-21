import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

session = fastf1.get_session(2023, 'Monaco', 'Q')
session.load()

def load_driver_data(driver):
    lap = session.laps.pick_driver(driver).pick_fastest()
    car_data = lap.get_car_data()
    time = car_data['Time']
    speed = car_data['Speed']
    style = fastf1.plotting.get_driver_style(identifier=driver, style=['color', 'linestyle'], session=session)
    data = {'Time': time, 'Speed': speed, 'Driver': driver}
    driver_colours.append(style)
    return data


if __name__ == "__main__":
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

    drivers = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS']
    driver_colours = []
    dataframe = pd.DataFrame()

    for driver in drivers:
        dataframe = pd.concat([dataframe, pd.DataFrame(load_driver_data(driver))], ignore_index=True)

    fig, ax = plt.subplots(3, 2, figsize=(16, 8))
    ax = ax.flatten()
    
    for index, axis in enumerate(ax):
        driver_data = dataframe[dataframe['Driver'] == drivers[index]]
        axis.plot(driver_data['Time'], driver_data['Speed'], label=drivers[index], **driver_colours[index])
        axis.set_title(f'{driver} Speed during Monaco 2023 Qualifying')
        axis.set_xlabel('Time (s)')
        axis.set_ylabel('Speed (km/h)')
        axis.legend()
    plt.tight_layout()
    plt.show()

