from typing import List, Union, Dict, Callable, cast
import argparse
import sys
import numpy as np
import app.double_pendulum_functions as dpf

Primitive = Union[str, bool, int, float]


def parse_args(args: List[str]) -> Dict[str, Primitive]:
    def greater_than(parameter: float) -> Callable[[str], float]:
        def function(string: str) -> float:
            value = float(string)
            if value <= parameter:
                raise argparse.ArgumentTypeError(f'The value {string} has to be greater than {parameter}.')
            return value

        return function

    def less_than_or_equal(parameter: float) -> Callable[[str], float]:
        def function(string: str) -> float:
            value = float(string)
            if value > parameter:
                raise argparse.ArgumentTypeError(f'The value {string} has to be less than or equal to {parameter}.')
            return value

        return function

    parser = argparse.ArgumentParser()
    parser.add_argument('--l1', nargs='?', type=greater_than(0.0), const=1.0, default=1.0,
                        help='The length of the first rod in meters. Default is 1.0.')
    parser.add_argument('--l2', nargs='?', type=greater_than(0.0), const=1.0, default=1.0,
                        help='The length of the second rod in meters. Default is 1.0.')

    parser.add_argument('--m1', nargs='?', type=greater_than(0.0), const=1.0, default=1.0,
                        help='The length of the first ball in kilograms. Default is 1.0.')
    parser.add_argument('--m2', nargs='?', type=greater_than(0.0), const=1.0, default=1.0,
                        help='The length of the second ball in kilograms. Default is 1.0.')

    # We want the default angle to be non-zero, or the pendulum will stay on top and not move.
    parser.add_argument('--o1', nargs='?', type=float, const=175.0, default=175.0,
                        help='The initial angle of the first pendulum in degrees. Default is 175.0.')
    parser.add_argument('--o2', nargs='?', type=float, const=175.0, default=175.0,
                        help='The initial angle of the second pendulum in degrees. Default is 175.0.')

    parser.add_argument('--w1', nargs='?', type=float, const=0.0, default=0.0,
                        help='The initial angular speed of the first pendulum in degrees per second. Default is 0.0.')
    parser.add_argument('--w2', nargs='?', type=float, const=0.0, default=0.0,
                        help='The initial angular speed of the second pendulum in degrees per second. Default is 0.0.')

    parser.add_argument('--t_max', nargs='?', type=greater_than(1.0), const=60.0, default=60.0,
                        help='The upper time bound in seconds. t_max is inclusive. The lower time bound is zero.'
                             'Default is 60.0. Has to be greater than 1.0.')
    parser.add_argument('--dt', nargs='?', type=less_than_or_equal(0.01), const=0.01, default=0.01,
                        help='The time step in seconds. Default is 0.01. Has to be less than 0.01')

    arg_dict = vars(parser.parse_args(args))

    return arg_dict


def main(args) -> None:
    arg_dict = parse_args(args)

    # Convert the degrees to radians. I made the input degrees because degrees are easier for people to understand.
    deg_to_rad = lambda x: x * np.pi / 180
    o1 = deg_to_rad(arg_dict['o1'])
    w1 = deg_to_rad(arg_dict['w1'])
    o2 = deg_to_rad(arg_dict['o2'])
    w2 = deg_to_rad(arg_dict['w2'])

    # Make these casts for mypy to be happy. Everything is a float.
    dict: Dict[str, float] = {key: cast(float, value) for key, value in arg_dict.items()}

    initials_positions = np.array([o1, w1, o2, w2])

    time_positions = dpf.integrate(initials_positions, dict['l1'], dict['l2'], dict['m1'], dict['m2'], dict['t_max'],
                                   dict['dt'])

    dpf.make_animations(time_positions, dict['l1'], dict['l2'])


if __name__ == "__main__":
    main(sys.argv[1:])
