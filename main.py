import fastf1
import matplotlib.pyplot as plt
import numpy as np

session = fastf1.get_session(2023, 'Monaco', 'Q')
session.load()

lec = session.laps.pick_driver('LEC').pick_fastest()
ham = session.laps.pick_driver('HAM').pick_fastest()
lec_car_data = lec.get_car_data()
ham_car_data = ham.get_car_data()

t_lec = lec_car_data['Time']
v_lec = lec_car_data['Speed']
t_ham = ham_car_data['Time']
v_ham = ham_car_data['Speed']

fig, ax = plt.subplots()
ax.plot(t_lec, v_lec, label='Leclerc', color='red')
ax.plot(t_ham, v_ham, label='Hamilton', color='blue')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Speed (km/h)')
ax.set_title('Leclerc and Hamilton Speed during Monaco 2023 Qualifying')
ax.legend()
plt.show()  
