"""
This module contains the base class for SimulatedObjects that don't have a controller. Instead they receive their pose
data from a motion capture system (in our case, most likely Optitrack).

Classes:
    MocapObject
"""

import xml.etree.ElementTree as ET
from abc import abstractmethod
import mujoco
from typing import Optional

from aiml_virtual.simulated_object import simulated_object


class MocapObject(simulated_object.SimulatedObject):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_identifiers(cls) -> Optional[list[str]]:
        # returning None opts out of XML parsing
        return None

    @abstractmethod
    def bind_to_data(self, data: mujoco.MjData):
        pass

    @abstractmethod
    def update(self, mj_step_count: int, step: float) -> None:
        pass

    @abstractmethod
    def create_xml_element(self, pos: str, quat: str, color: str) -> dict[str, list[ET.Element]]:
        pass

