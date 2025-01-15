"""
This script shows how to load and display a simulation from an xml.
"""

import os
import sys
import pathlib

# The lines under here are intended to make sure imports work, by adding parent folders to the path (i.e. the list
# of folders where the interpreter will look for a given package when you try to import it). This is to account for
# differences in what the interpreter identifies as your current working directory when launching these scripts
# from the command line as regular scripts vs with the -m option vs from PyCharm, as well as the script being placed
# in any depth of sub-sub-subfolder.
project_root = pathlib.Path(__file__).parents[0]
sys.path.append(project_root.resolve().as_posix())  # add the folder this file is in to path
# until we meet the "aiml_virtual" package, keep adding the current folder to the path and then changing folder into
# the parent folder
while "aiml_virtual" not in [f.name for f in  project_root.iterdir()]:
    project_root = project_root.parents[0]
    sys.path.append(project_root.resolve().as_posix())
import aiml_virtual
xml_directory = aiml_virtual.xml_directory
from aiml_virtual import scene, simulator

from aiml_virtual.mocap import optitrack_mocap_source

if __name__ == "__main__":
    scn = scene.Scene(os.path.join(xml_directory, "scene_base.xml"), save_filename="test.xml")
    mocap = optitrack_mocap_source.OptitrackMocapSource()
    scn.add_mocap_objects(mocap)
    sim = simulator.Simulator(scn)
    with sim.launch():
        while sim.viewer.is_running():
            sim.tick()  # tick steps the simulator, including all its subprocesses