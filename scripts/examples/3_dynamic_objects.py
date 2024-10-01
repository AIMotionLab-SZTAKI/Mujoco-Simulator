"""
This script shows how dynamic objects work.
"""

import os
import sys
import pathlib
import numpy as np

# make sure imports work by adding the necessary folders to the path:
project_root = pathlib.Path(__file__).parents[0]
sys.path.append(project_root.resolve().as_posix())  # add the folder this file is in to path
# until we meet the "aiml_virtual" package, keep adding the current folder to the path and then changing folder into
# the parent folder
while "aiml_virtual" not in [f.name for f in  project_root.iterdir()]:
    project_root = project_root.parents[0]
    sys.path.append(project_root.resolve().as_posix())
xml_directory = os.path.join(project_root.resolve().as_posix(), "xml_models")
project_root = project_root.resolve().as_posix()

from aiml_virtual import scene, simulator
from aiml_virtual.trajectory import dummy_drone_trajectory, skyc_trajectory
from aiml_virtual.simulated_object.dynamic_object import dynamic_object
from aiml_virtual.simulated_object.dynamic_object.controlled_object import bicycle
from aiml_virtual.simulated_object.dynamic_object.controlled_object.drone import crazyflie, bumblebee

if __name__ == "__main__":
    # As mentioned in 2_build_scene.py, we can simulate physics using DynamicObjects. So far we've only seen dynamic
    # objects that had no actuators. Let's change that, and build a scene with dynamic objects based on the empty
    # checkerboard scene base!
    scn = scene.Scene(os.path.join(xml_directory, "empty_checkerboard.xml"), save_filename=f"example_scene_3.xml")

    # A bicycle is the simplest actuated object, with a motor at the rear wheel with a set torque.
    bike = bicycle.Bicycle()
    scn.add_object(bike, "0 1 0.1", "1 0 0 0", "0.5 0.5 0.5 1")

    # A bumblebee is only interesting if it actually flies. In order to fly, it needs a trajectory to follow. At its
    # most basic, a trajectory is a DummyDroneTrajectory, with a fixed setpoint.
    bb = bumblebee.Bumblebee()
    bb.trajectory = dummy_drone_trajectory.DummyDroneTrajectory(np.array([-1, 0, 0.5]))
    scn.add_object(bb, "-1 0 0.5", "1 0 0 0", "0.5 0.5 0.5 1")
    # In order to give the bumblebee's controller some work, let's add a non-actuated dynamic object that drops from
    # the sky and disturbs the bumblebee:
    scn.add_object(dynamic_object.DynamicPayload(), "-0.9 0 1")

    # The dummy trajectory may have seemed a bit boring, even with the disturbance. A more interesting trajectory type
    # is read from a skyc file. An example skyc file is found under scripts/misc/skyc_example.skyc
    cf = crazyflie.Crazyflie()
    traj = skyc_trajectory.SkycTrajectory(f"{project_root}/scripts/misc/skyc_example.skyc")
    cf.trajectory = traj
    scn.add_object(cf, "0 0 0", "1 0 0 0", "0.5 0.5 0.5 1")

    sim = simulator.Simulator(scn, update_freq=500, target_fps=100)
    with sim.launch_viewer():
        while sim.viewer.is_running():
            sim.tick()  # tick steps the simulator, including all its subprocesses



