import numpy as np
from typing import Optional, cast, Type
from scipy.spatial.transform import Rotation

from aiml_virtual.simulated_object.mocap_object import mocap_object
from aiml_virtual.mocap import mocap_source
from aiml_virtual.simulated_object.mocap_object.mocap_drone.mocap_bumblebee import MocapBumblebee
from aiml_virtual.simulated_object.mocap_object.mocap_object import MocapHook
from aiml_virtual.simulated_object.mocap_skeleton import mocap_skeleton

from aiml_virtual.utils import utils_general
warning = utils_general.warning

class MocapHookedBumblebee2DOF(mocap_skeleton.MocapSkeleton):
    configurations: dict[str, list[str]] = {
        "bb3": [("bb3", MocapBumblebee), ("hook12", MocapHook)]
    }

    @classmethod
    def get_identifier(cls) -> Optional[str]:
        return "MocapHookedBumblebee2DOF"

    def __init__(self, source: mocap_source.MocapSource, mocap_name: str):
        super().__init__(source, mocap_name)
        self.bumblebee: MocapBumblebee =  cast(MocapBumblebee, self.mocap_objects[0])
        self.hook: mocap_object.MocapHook = cast(mocap_object.MocapHook, self.mocap_objects[1])

    def update(self) -> None:
        if self.source is not None:
            mocap_frame = self.source.data
            self.bumblebee.spin_propellers()
            if self.bumblebee.mocap_name in mocap_frame and self.hook.mocap_name in mocap_frame:
                bb_pos, bb_quat = mocap_frame[self.bumblebee.mocap_name]
                bb_offset = self.bumblebee.offset
                bb_rotmat = Rotation.from_quat(np.roll(bb_quat, -1)).as_matrix()
                bb_pos += bb_rotmat @ bb_offset
                hook_pos, hook_quat = mocap_frame[self.hook.mocap_name]
                self.data.mocap_pos[self.bumblebee.mocapid] = bb_pos
                self.data.mocap_quat[self.bumblebee.mocapid] = bb_quat
                self.data.mocap_quat[self.hook.mocapid] = hook_quat
                hook_offset_drone_frame = np.array([0.03, 0, -0.03])
                hook_offset_world_frame = bb_rotmat @ hook_offset_drone_frame
                self.data.mocap_pos[self.hook.mocapid] = bb_pos + hook_offset_world_frame
        else:
            warning(f"Obj {self.name} Mocap is none.")
            return