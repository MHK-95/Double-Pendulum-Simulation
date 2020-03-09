from typing import Tuple, List, Union, Iterable
import numpy as np
from numpy.core._multiarray_umath import ndarray
import scipy.constants
import scipy.integrate
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os
import os.path as osp
import ffmpeg
import glob

g = scipy.constants.g
this_dir = osp.dirname(osp.realpath(__file__))


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
        -> ndarray:
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
    :return: A 2D ndarray of 5 columns of [[t, o1, w1, o2, w2], ...]
    """
    t_array = np.arange(0, t_max + dt, dt)
    position_array = scipy.integrate.odeint(pendulum_derivatives, initial_positions, t_array, args=(l1, l2, m1, m2))
    t_array = t_array.reshape(t_array.size, 1)  # Convert the 1D array to a 2D array of single columns
    return np.append(t_array, position_array, 1)


def print_bold(message: str) -> None:
    print(f"\033[1m{message}\033[0m", flush=True)


def make_animations(time_positions, l1, l2) -> None:
    t, theta1, theta2 = time_positions[:, 0], time_positions[:, 1], time_positions[:, 3]
    dt = t[1] - t[0]

    # Convert to Cartesian coordinates of the two bob positions.
    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)
    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)

    # Plotted bob circle radius
    circle_radius = 0.15
    # Plot a trail of the m2 bob's position for the last trail_secs seconds.
    trail_secs = 1
    # This corresponds to max_trail time points.
    max_trail = int(trail_secs / dt)

    def make_single_frame(i: int) -> None:
        # Plot and save an image of the double pendulum configuration for time point i.
        # The pendulum rods.
        ax.plot([0, x1[i], x2[i]], [0, y1[i], y2[i]], lw=2, c='k')
        # Circles representing the anchor point of rod 1, and bobs 1 and 2.
        c0 = Circle((0, 0), circle_radius / 2, fc='k', zorder=10)
        c1 = Circle((x1[i], y1[i]), circle_radius, fc='b', ec='b', zorder=10)
        c2 = Circle((x2[i], y2[i]), circle_radius, fc='r', ec='r', zorder=10)
        ax.add_patch(c0)
        ax.add_patch(c1)
        ax.add_patch(c2)

        # Make a trail for each of the Pendulums
        ns = 20  # The trail will be divided into 20 ns segments and plotted as a fading line.
        s = max_trail // ns

        for j in range(ns):
            i_min = i - (ns - j) * s
            if i_min < 0:
                continue
            i_max = i_min + s + 1
            alpha = (j / ns) ** 2
            ax.plot(x1[i_min:i_max], y1[i_min:i_max], c='b', solid_capstyle='butt', lw=2, alpha=alpha)
            ax.plot(x2[i_min:i_max], y2[i_min:i_max], c='r', solid_capstyle='butt', lw=2, alpha=alpha)

        total_radius = l1 + l2 + circle_radius
        ax.set_xlim(-total_radius, total_radius)
        ax.set_ylim(-total_radius, total_radius)
        ax.set_aspect('equal', adjustable='box')
        plt.axis('off')
        plt.savefig(osp.join(this_dir, 'frames', 'img_{:05d}.png'.format(i // di)), dpi=72)
        plt.cla()

    # Make an image every di time points, corresponding to a frame rate of fps 10 frames per second.
    fps = 10
    di = int(1 / fps / dt)
    fig = plt.figure(figsize=(8.3333, 6.25), dpi=72)
    ax = fig.add_subplot(111)

    print_bold('\nMaking the frames.')
    for i in range(0, t.size, di):
        make_single_frame(i)

    print_bold('\nMaking the mp4 animation.')
    (
        ffmpeg
            .input(osp.join(this_dir, 'frames', 'img_*.png'), pattern_type='glob', framerate=10)
            .output(osp.join(this_dir, 'animations', 'double_pendulum_example.mp4'))
            .run(quiet=True, overwrite_output=True)
    )

    print_bold('\nMaking the gif animation.')
    (
        ffmpeg
            .input(osp.join(this_dir, 'frames', 'img_*.png'), pattern_type='glob', framerate=10)
            .output(osp.join(this_dir, 'animations', 'double_pendulum.gif'))
            .run(quiet=True, overwrite_output=True)
    )

    print_bold('\nDeleting all the frames.')
    for f in glob.glob(osp.join(this_dir, 'frames', 'img_*.png')):
        os.remove(f)

    print_bold('\nDone!')
