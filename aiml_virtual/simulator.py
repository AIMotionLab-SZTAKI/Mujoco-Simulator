"""
Module that contains the class handling simulation.
"""

import math
import mujoco
import mujoco.viewer
from typing import Optional, Callable
from contextlib import contextmanager
import platform
import glfw
if platform.system() == 'Windows':
    import win_precise_time as time
else:
    import time


from aiml_virtual import scene
from aiml_virtual.simulated_object import simulated_object
from aiml_virtual import utils

Scene = scene.Scene
SimulatedObject = simulated_object.SimulatedObject

class Simulator:
    """
    Class that uses the scene and the mujoco package to run the mujoco simulation and display the results.
    """
    def __init__(self, scene: Scene, control_freq: float = 100, target_fps: int = 50):
        self.scene: Scene = scene  #: The scene corresponding to the mujoco model.
        self.data: mujoco.MjData = mujoco.MjData(self.model)  #: The data corresponding to the model.
        self.viewer: Optional[mujoco.viewer.Handle] = None  #: The handler to be used for the passive viewer.
        self.mj_step_count: int = 0  #: The numer of times the physics loop (mj_step) was called.
        self.processes: list[tuple[Callable, int]] = []  #: The list of what function to call after however many physics steps.
        self.time = utils.PausableTime()  #: The inner timer of the simulation.
        self.callback_dictionary: dict[int, callable] = {
            glfw.KEY_SPACE: self.toggle_pause
        }  #: A dictionary of what function to call when receiving a given keypress.

        self.add_process(self.update_objects, control_freq)
        self.add_process(self.sync, target_fps)

    @property
    def physics_step(self) -> float:
        """
        Property to grab the timestep of a physics iteration from the model.
        """
        return self.opt.timestep

    @property
    def opt(self) -> mujoco.MjOption:
        """
        Property to grab the options from the model.
        """
        return self.model.opt

    @property
    def simulated_objects(self):
        """
        Property to grab the list of objects in the scene.
        """
        return self.scene.simulated_objects

    @property
    def model(self) -> mujoco.MjModel:
        """
        Property to grab the mujoco model from the scene.
        """
        return self.scene.model

    @property
    def paused(self) -> bool:
        """
        Property to grab whether the simulation is currently running.
        """
        return not self.time.ticking

    def toggle_pause(self) -> None:
        """
        Pauses the simulation if it's running; resumes it if it's paused.
        """
        if self.paused:
            self.time.resume()
        else:
            self.time.pause()

    @contextmanager
    def launch_viewer(self) -> 'Simulator':
        """
        Wraps the mujoco.viewer.launch_passive function so that it handlers the simulator's initialization. As this
        is a context handler, it should be used like so:

        .. code-block:: python

            sim = simulator.Simulator(scene, control_freq=500, target_fps=100)
            with sim.launch_viewer():
                while sim.viewer.is_running():
                    sim.step()

        """
        self.bind_scene()
        try:
            mujoco.mj_step(self.model, self.data)  # TODO: look up: I think we need a 0th step?
            self.time.reset()
            self.viewer = mujoco.viewer.launch_passive(self.model, self.data, show_left_ui=False, show_right_ui=False,
                                                       key_callback=self.handle_keypress)
            yield self
        finally:
            if self.viewer:
                self.viewer.close()
                self.viewer = None

    def bind_scene(self) -> None:
        for obj in self.simulated_objects:
            obj.bind_to_data(self.data)

    def add_process(self, method: Callable, frequency: float) -> None:
        """Register a process to be run at a specified frequency.

        Args:
            method (function): The method of the Simulator class to run.
            frequency (float): The frequency (in Hz) at which to run the method.
        """
        # the method we're registering shall be called after interval number of physics loops, for example, if
        # the physics step is 1ms, and the control frequency is 100Hz, then the method calculating control inputs
        # must be called every 10th physics loop
        interval = max(1, math.ceil((1 / frequency) / self.physics_step))
        self.processes.append((method, interval))

    def step(self) -> None:
        # this is the function that steps the mujoco simulator, and calls all the other processes
        for method, interval in self.processes:  # each process must be registered
            if self.mj_step_count % interval == 0:
                method()  # maybe arguments? we'll see
        # We may wish to do some optimization here: if each process step time (interval) is an integer multiple of
        # the process that's closest to it in frequency, then we can save some time by calling mj_step with an extra
        # argument nstep. This nstep may be the interval of the fastest process.
        # For example, if the physics is 1000Hz, the control is 100Hz, and the display is 50Hz, then we can call the
        # physics engine for 10 steps at every loop, call the control every loop and the display every other loop
        # TODO: think through whether this needs to be reconciled with data.time and whether it needs to be moved inside
        #  the if condition under here
        dt = self.data.time - self.time()
        if dt > 0:  # if the simulation needs to wait in order to not run ahead
             time.sleep(dt)
        if not self.paused:
            mujoco.mj_step(self.model, self.data)
            self.mj_step_count += 1

    def update_objects(self) -> None:
        for obj in self.simulated_objects:
            obj.update(self.mj_step_count, self.physics_step)

    def sync(self) -> None:
        # print(f"time: {self.data.time}")
        self.viewer.sync()

    def handle_keypress(self, keycode) -> None:
        self.callback_dictionary[keycode]()

