from typing import Tuple, List, Union, Iterable
import numpy as np
from numpy.core._multiarray_umath import ndarray
import scipy.constants
import scipy.integrate

g = scipy.constants.g


def lagrangian_1(positions: ndarray, l1: float, l2: float, m1: float, m2: float) -> float:
    """
    Will return the angular acceleration of the first pendulum.

    :param positions: 4D np array of [angle 1, angular velocity 1, angle 2, angular velocity 2] in radians and radians
    per second
    :param t: Time parameter in seconds. Is not actually being used.
    :param l1: Rod length of the first pendulum in meters.
    :param l2: Rod length of the second pendulum in meters.
    :param m1: Mass of the first ball in kg.
    :param m2: Mass of the second ball in kg
    :return: angular acceleration 1
    """
    o1, w1, o2, w2 = positions
    s, c = np.sin(o2 - o1), np.cos(o2 - o1)

    a1 = m2 * l1 * s * c * w1 ** 2
    a2 = m2 * g * np.sin(o2) * c
    a3 = m2 * l2 * s * w2 ** 2
    a4 = (m1 + m2) * g * np.sin(o1)

    b1 = (m1 + m2) * l1
    b2 = m2 * l1 * c ** 2

    return (a1 + a2 + a3 - a4) / (b1 - b2)


def lagrangian_2(positions: ndarray, l1: float, l2: float, m1: float, m2: float) -> float:
    """
    Will return the angular acceleration of the second pendulum.

    :param positions: 4D np array of [angle 1, angular velocity 1, angle 2, angular velocity 2] in radians and radians
    per second
    :param t: Time parameter in seconds. Is not actually being used.
    :param l1: Rod length of the first pendulum in meters.
    :param l2: Rod length of the second pendulum in meters.
    :param m1: Mass of the first ball in kg.
    :param m2: Mass of the second ball in kg
    :return: angular acceleration 2
    """
    o1, w1, o2, w2 = positions
    s, c = np.sin(o2 - o1), np.cos(o2 - o1)

    a1 = m2 * l2 * s * c * w2 ** 2
    a2 = g * np.sin(o1) * c
    a3 = l1 * s * w1 ** 2
    a4 = g * np.sin(o2)

    b1 = (m1 + m2) * l2
    b2 = m2 * l2 * c ** 2

    return ((m1 + m2) * (a2 - a3 - a4) - a1) / (b1 - b2)


def pendulum_derivatives(positions: ndarray, t: float, l1: float, l2: float, m1: float, m2: float) \
        -> Tuple[float, float, float, float]:
    """
    Will return the derivatives of the angles and angular velocity.

    :param positions: 4D np array of [angle 1, angular velocity 1, angle 2, angular velocity 2] in radians and radians
    per second
    :param t: Time parameter in seconds. Is not actually being used.
    :param l1: Rod length of the first pendulum in meters.
    :param l2: Rod length of the second pendulum in meters.
    :param m1: Mass of the first ball in kg.
    :param m2: Mass of the second ball in kg
    :return: Tuple of (angular velocity 1, angular acceleration 1, angular velocity 2, angular acceleration 2)
    """
    o1, w1, o2, w2 = positions

    angular_velocity_1 = w1
    angular_acceleration_1 = lagrangian_1(positions, l1, l2, m1, m2)
    angular_velocity_2 = w2
    angular_acceleration_2 = lagrangian_2(positions, l1, l2, m1, m2)
    return angular_velocity_1, angular_acceleration_1, angular_velocity_2, angular_acceleration_2


def map_to_cartesian_coordinates(o1: float, o2: float, l1: float, l2: float) -> ndarray:
    """
    Will return the positions of the pendulums to cartesian coordinates in meters.

    :param o1: The angle in radians of the first pendulum.
    :param o2: The angle in radians of the second pendulum.
    :param l1: Rod length of the first pendulum in meters.
    :param l2: Rod length of the second pendulum in meters.
    :return: ndarray of (x1, y1, x2, y2)
    """
    x1 = l1 * np.sin(o1)
    y1 = l1 * np.cos(o1)

    x2 = x1 + l2 * np.sin(o2)
    y2 = y1 + l2 * np.cos(o2)

    return np.array([x1, y1, x2, y2])


def calculate_total_energy(positions: ndarray, l1, l2, m1, m2) -> float:
    """
    :param positions: 4D np array of [angle 1, angular velocity 1, angle 2, angular velocity 2] in radians and radians
    per second
    :param l1: Rod length of the first pendulum in meters.
    :param l2: Rod length of the second pendulum in meters.
    :param m1: Mass of the first ball in kg.
    :param m2: Mass of the second ball in kg
    :return: The total energy of the system in Joules.
    """
    o1, w1, o2, w2 = positions.T

    a1 = -(m1 + m2) * l1 * g * np.cos(o1)
    a2 = -m2 * l2 * g * np.cos(o2)

    V = a1 + a2

    b1 = 0.5 * m1 * (l1 * w1) ** 2
    b2 = (l1 * w1) ** 2
    b3 = (l2 * w2) ** 2
    b4 = 2 * l1 * l2 * w1 * w2 * np.cos(o1 - o2)

    T = b1 + 0.5 * m2 * (b2 + b3 + b4)

    return T + V


def integrate(initial_positions: ndarray, l1: float, l2: float, m1: float, m2: float, t_max: float, dt: float) \
        -> List[Tuple[float, ndarray]]:
    """
    Will numerically integrate the double pendulum derivatives and return the time steps of the positions of the
    pendulums. The time steps will be from 0 to t_max.

    :param initial_positions: The initial starting positions. 4D np array of [angle 1, angular velocity 1, angle 2,
    angular velocity 2] in radians and radians per second
    :param l1: Rod length of the first pendulum in meters.
    :param l2: Rod length of the second pendulum in meters.
    :param m1: Mass of the first ball in kg.
    :param m2: Mass of the second ball in kg
    :param t_max: The maximum time boundary. t_max is inclusive.
    :param dt: The time step.
    :return: A List of Tuples, where the first tuple element is the time and the second tuple element is the ndarray of
    the positions
    """
    t_array = np.arange(0, t_max + dt, dt)
    position_list = scipy.integrate.odeint(pendulum_derivatives, initial_positions, t_array, args=(l1, l2, m1, m2))
    return list(zip(t_array, position_list))
