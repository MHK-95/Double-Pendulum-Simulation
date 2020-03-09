import pytest
import numpy as np
import app.double_pendulum_functions as dpf

"""
It's hard to unit test the double pendulum functions since it relies on numerical integration and there will be
numerical errors. The numerical errors will grow in the form of random walk as the simulation continues for a long time. 

We can test that the simulation is accurate by checking if the total energy is conserved in the system. This will also 
use almost all the functions in the double_pendulum_functions and give us almost 100% code coverage.
"""


def test_energy():
    """
    Test if the energy drift is not too big. Test if the final energy of the system is within 1 percent range of the
    initial energy of the system. It will be 1,000 steps with a dt of 0.01 seconds. The total energy of the system,
    should decrease with time. The system slowly loses energy.
    """
    l1, l2 = 1, 1
    m1, m2 = 1, 1
    t_max, dt = 10_00, 0.01
    initial_positions = np.array([2 * np.pi / 3, 31, 3 * np.pi / 4, 21])

    time_positions = dpf.integrate(initial_positions, l1, l2, m1, m2, t_max, dt)

    initial_energy = dpf.calculate_total_energy(time_positions[0, 1:5], l1, l2, m1, m2)
    final_energy = dpf.calculate_total_energy(time_positions[-1, 1:5], l1, l2, m1, m2)

    energy_change_percentage = abs((final_energy - initial_energy) / initial_energy * 100)

    assert energy_change_percentage <= 1
