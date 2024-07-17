import math
import numpy as np
from cuboid_array import CuboidArray

class WindSampler:
    def __init__(self, wind_data_filename):
        self._wind_data = CuboidArray(wind_data_filename)

    def generate_forces(self, drone):
        drone_state = drone.get_state_copy()
        drone_velocity = drone_state["vel"]
        drone_position = drone_state["pos"]

        wind_speed = self._wind_data.get_corresponding_velocity(drone_position)
        x = wind_speed - drone_speed
        ALPHA = np.power(10, -2) * np.array([3.3, 2.7, 2.2])
        phi = np.diag(x)
        return np.dot(phi, ALPHA)