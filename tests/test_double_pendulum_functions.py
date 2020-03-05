import pytest
import numpy as np
import main.double_pendulum_functions as pd
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
    t_max, dt = 1_000, 0.01
    initial_positions = np.array([2 * np.pi / 3, 0, 3 * np.pi / 4, 0])
    initial_energy = pd.calculate_total_energy(initial_positions, l1, l2, m1, m2)

    position_list = pd.integrate(initial_positions, l1, l2, m1, m2, t_max, dt)
    final_energy = pd.calculate_total_energy(position_list[-1][1], l1, l2, m1, m2)
    energy_change_percentage = abs((final_energy - initial_energy) / initial_energy * 100)

    assert energy_change_percentage <= 1


def test_cartesian_coordinates():
    """
    Test to see if the conversion to cartesian coordinates is correct.
    """
    expected_result = np.array([0, 1, 0, 2])
    actual_result = pd.map_to_cartesian_coordinates(0, 0, 1, 1)
    assert np.allclose(expected_result, actual_result)

    expected_result = np.array([1, 0, 2, 0])
    actual_result = pd.map_to_cartesian_coordinates(1/2*np.pi, 1/2*np.pi, 1, 1)
    assert np.allclose(expected_result, actual_result)

    expected_result = np.array([0, -1, 0, -2])
    actual_result = pd.map_to_cartesian_coordinates(np.pi, np.pi, 1, 1)
    assert np.allclose(expected_result, actual_result)

    expected_result = np.array([-1, 0, -2, 0])
    actual_result = pd.map_to_cartesian_coordinates(3/2*np.pi, 3/2*np.pi, 1, 1)
    assert np.allclose(expected_result, actual_result)

    expected_result = np.array([0, 1, 0, 2])
    actual_result = pd.map_to_cartesian_coordinates(2*np.pi, 2*np.pi, 1, 1)
    assert np.allclose(expected_result, actual_result)
