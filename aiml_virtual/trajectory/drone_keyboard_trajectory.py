from aiml_virtual.trajectory.trajectory_base import TrajectoryBase
from aiml_virtual.util import mujoco_helper
import numpy as np


class DroneKeyboardTraj(TrajectoryBase):

    def __init__(self, load_mass, target_pos):
        super().__init__()
        self.load_mass = load_mass
        self.target_pos = np.copy(target_pos)
        self.target_rpy = np.array((0.0, 0.0, 0.0))

        self.speed = 0.04
        self.rot_speed = 0.004

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        self.w_pressed = False
    
    
    def evaluate(self, state, i, time, control_step):

        if self.up_pressed:
            self.move_forward(state)
        
        if self.down_pressed:
            self.move_backward(state)

        if self.left_pressed:
            self.move_left(state)

        if self.right_pressed:
            self.move_right(state)
        
        if self.a_pressed:
            self.rot_left(state)
        
        if self.d_pressed:
            self.rot_right(state)
        
        if self.w_pressed:
            self.move_up(state)
            
        if self.s_pressed:
            self.move_down(state)

        self.output["load_mass"] = self.load_mass
        self.output["target_pos"] = self.target_pos
        self.output["target_rpy"] = self.target_rpy
        self.output["target_vel"] = np.array((0.0, 0.0, 0.0))
        self.output["target_pos_load"] = np.array((0.0, 0.0, 0.0))
        self.output["target_eul"] = np.zeros(3)
        self.output["target_pole_eul"] = np.zeros(2)
        self.output["target_ang_vel"] = np.zeros(3)
        self.output["target_pole_ang_vel"] = np.zeros(2)
        return self.output

    def up_press(self):
        self.up_pressed = True
    
    def up_release(self):
        self.up_pressed = False
    
    def down_press(self):
        self.down_pressed = True
    
    def down_release(self):
        self.down_pressed = False
    
    def left_press(self):
        self.left_pressed = True
    
    def left_release(self):
        self.left_pressed = False
    
    def right_press(self):
        self.right_pressed = True
    
    def right_release(self):
        self.right_pressed = False
    
    def a_press(self):
        self.a_pressed = True
    
    def a_release(self):
        self.a_pressed = False
    
    def s_press(self):
        self.s_pressed = True
    
    def s_release(self):
        self.s_pressed = False
    
    def d_press(self):
        self.d_pressed = True
    
    def d_release(self):
        self.d_pressed = False
    
    def w_press(self):
        self.w_pressed = True
    
    def w_release(self):
        self.w_pressed = False
    
    def move_forward(self, state):
        diff = mujoco_helper.qv_mult(state["quat"], np.array((self.speed, 0.0, 0.0)))
        diff[2] = 0.0
        self.target_pos += diff
        
    def move_backward(self, state):
        diff = mujoco_helper.qv_mult(state["quat"], np.array((self.speed, 0.0, 0.0)))
        diff[2] = 0.0
        self.target_pos -= diff
    
    def move_left(self, state):
        diff = mujoco_helper.qv_mult(state["quat"], np.array((0.0, self.speed, 0.0)))
        diff[2] = 0.0
        self.target_pos += diff
    
    def move_right(self, state):
        diff = mujoco_helper.qv_mult(state["quat"], np.array((0.0, self.speed, 0.0)))
        diff[2] = 0.0
        self.target_pos -= diff
    
    def move_up(self, state):

        self.target_pos[2] += self.speed / 3.0
    
    def move_down(self, state):

        self.target_pos[2] -= self.speed

    def rot_left(self, state):

        self.target_rpy[2] += self.rot_speed
        #print(self.target_rpy)
    
    def rot_right(self, state):

        self.target_rpy[2] -= self.rot_speed
        #print(self.target_rpy)