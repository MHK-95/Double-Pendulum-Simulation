from typing import List, Union, Dict
import argparse
import sys
import numpy

Primitive = Union[str, bool, int, float]


def parse_args(args: List[str]) -> Dict[str, Primitive]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--l1', nargs='?', type=float, const=1.0, default=1.0,
                        help='The length of the first rod in meters. Default is 1.0.')
    parser.add_argument('--l2', nargs='?', type=float, const=1.0, default=1.0,
                        help='The length of the second rod in meters. Default is 1.0.')

    parser.add_argument('--m1', nargs='?', type=float, const=1.0, default=1.0,
                        help='The length of the first ball in kilograms. Default is 1.0.')
    parser.add_argument('--m2', nargs='?', type=float, const=1.0, default=1.0,
                        help='The length of the second ball in kilograms. Default is 1.0.')

    # We want the default angle to be non-zero, or the pendulum will stay on top and not move.
    parser.add_argument('--o1', nargs='?', type=float, const=15.0, default=15.0,
                        help='The initial angle of the first pendulum in degrees. Default is 15.0.')
    parser.add_argument('--o2', nargs='?', type=float, const=15.0, default=15.0,
                        help='The initial angle of the second pendulum in degrees. Default is 15.0.')

    parser.add_argument('--w1', nargs='?', type=float, const=0.0, default=0.0,
                        help='The initial angular speed of the first pendulum in degrees per second. Default is 0.0.')
    parser.add_argument('--w2', nargs='?', type=float, const=0.0, default=0.0,
                        help='The initial angular speed of the second pendulum in degrees per second. Default is 0.0.')

    parser.add_argument('--t_max', nargs='?', type=float, const=60.0, default=60.0,
                        help='The upper time bound in seconds. t_max is inclusive. The lower time bound is zero.' 
                             'Default is 60.0.')
    parser.add_argument('--dt', nargs='?', type=float, const=0.01, default=0.01,
                        help='The time step in seconds. Default is 0.01.')

    arg_dict = vars(parser.parse_args(args))

    return arg_dict


def main() -> None:
    arg_dict = parse_args(sys.argv[1:])

    # Convert the degrees to radians. I made the input degrees because degrees are easier for people to understand.
    deg_to_rad = lambda x: x * np.pi/180
    arg_dict['o1'] = deg_to_rad(arg_dict['o1'])
    arg_dict['o2'] = deg_to_rad(arg_dict['o2'])
    arg_dict['w1'] = deg_to_rad(arg_dict['w1'])
    arg_dict['w2'] = deg_to_rad(arg_dict['w2'])


