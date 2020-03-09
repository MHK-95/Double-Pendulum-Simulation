import glob
import pytest
import app.main as main
import os
import os.path as osp


def test_parse_args():
    expected_output = {'l1': 1.0, 'l2': 1.0, 'm1': 1.0, 'm2': 1.0, 'o1': 175.0, 'o2': 175.0, 'w1': 0.0, 'w2': 0.0,
                       't_max': 60.0, 'dt': 0.01}
    actual_output = main.parse_args([])
    assert expected_output == actual_output

    actual_output = main.parse_args(['--l1', '--l2', '--m1', '--m2', '--o1', '--o2', '--w1', '--w2', '--t_max', '--dt'])
    assert expected_output == actual_output

    expected_output = {'l1': 2.0, 'l2': 2.0, 'm1': 2.0, 'm2': 2.0, 'o1': 2.0, 'o2': 2.0, 'w1': 2.0, 'w2': 2.0,
                       't_max': 2.0, 'dt': 0.00999999}
    actual_output = main.parse_args(['--l1', '2.', '--l2', '2.0000000', '--m1', '2', '--m2', '2.00', '--o1', '2.',
                                     '--o2', '2', '--w1', '2.0', '--w2', '2.0', '--t_max', '2', '--dt', '0.00999999'])
    assert expected_output == actual_output

    with pytest.raises(SystemExit):
        main.parse_args(['--l1', '213', '--w2', '--t_max', 'This_will_cause_an_error.'])

    with pytest.raises(SystemExit):
        main.parse_args(['--t_max', '1.000'])

    with pytest.raises(SystemExit):
        main.parse_args(['--dt', '0.010001'])

def test_main():
    this_dir = osp.dirname(osp.realpath(__file__))
    parent_dir = osp.split(this_dir)[0]

    gif_file = osp.join(parent_dir, 'app', 'animations', 'double_pendulum.gif')
    mp4_file = osp.join(parent_dir, 'app', 'animations', 'double_pendulum.mp4')

    # Remove files if they exist from the previous run.
    if osp.isfile(gif_file):
        os.remove(gif_file)

    if osp.isfile(mp4_file):
        os.remove(mp4_file)

    main.main([])

    # Check if the frames have been deleted.
    assert not glob.glob(osp.join(parent_dir, 'app', 'frames', 'img_*.png'))

    # Check if the gif has been created.
    assert osp.isfile(osp.join(parent_dir, 'app', 'animations', 'double_pendulum.gif'))

    # Check if the mp4 has been created.
    assert osp.isfile(osp.join(parent_dir, 'app', 'animations', 'double_pendulum.mp4'))
