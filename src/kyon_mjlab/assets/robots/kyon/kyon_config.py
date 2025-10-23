"""IIT Kyon constants."""

from pathlib import Path

import mujoco

from mjlab.entity import EntityArticulationInfoCfg, EntityCfg
from mjlab.utils.actuator import ElectricActuator, reflected_inertia
from mjlab.utils.os import update_assets
from mjlab.utils.spec_config import ActuatorCfg, CollisionCfg

import rospkg
rospack = rospkg.RosPack()

from kyon_mjlab.assets.utils.urdf_utils import (
    parse_xacro,
    add_mujoco_compiler_tag,
    resolve_package_paths,
)

import os

##
# MJCF and assets.
##

KYON_URDF_PATH = Path(rospack.get_path('kyon_urdf'))
KYON_XACRO: Path = KYON_URDF_PATH / "urdf" / "kyon.urdf.xacro"
assert KYON_XACRO.exists()

KYON_XACRO_ARGS = {
    'upper_body': os.environ.get('KYON_UPPER_BODY', 'false'),
    'wheels': os.environ.get('KYON_WHEELS', 'false'),
    'varta': os.environ.get('KYON_VARTA', 'true'),
    'add_collision': os.environ.get('KYON_ADD_COLLISION', 'false'),
}

KYON_URDF = parse_xacro(KYON_XACRO, KYON_XACRO_ARGS)
KYON_URDF = add_mujoco_compiler_tag(KYON_URDF)
KYON_URDF = resolve_package_paths(KYON_URDF)

def get_spec() -> mujoco.MjSpec:
  spec = mujoco.MjSpec.from_string(KYON_URDF)
  return spec

output_path = Path(__file__).parent / "generated" / "kyon_generated.xml"
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    f.write(get_spec().to_xml())

output_path = output_path.parent / "kyon_generated.urdf"
with open(output_path, "w") as f:
    f.write(KYON_URDF)    


##
# Actuator config.
##

# Rotor inertia.
# From experimental setup.
ROTOR_REFLECTED_INERTIA = 0.3

# Gearbox.
HIP_GEAR_RATIO = 50
KNEE_GEAR_RATIO = 50

HIP_ACTUATOR = ElectricActuator(
  reflected_inertia=ROTOR_REFLECTED_INERTIA,
  velocity_limit=7.0,
  effort_limit=100.0,
)
KNEE_ACTUATOR = ElectricActuator(
  reflected_inertia=ROTOR_REFLECTED_INERTIA,
  velocity_limit=7.0,
  effort_limit=100.0,
)

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS_HIP = 400.0
DAMPING_HIP = 10.0

STIFFNESS_KNEE = 400.0
DAMPING_KNEE = 10.0

KYON_HIP_ACTUATOR_CFG = ActuatorCfg(
  joint_names_expr=["hip_roll_.*", "hip_pitch_.*"],
  effort_limit=HIP_ACTUATOR.effort_limit,
  stiffness=STIFFNESS_HIP,
  damping=DAMPING_HIP,
  armature=HIP_ACTUATOR.reflected_inertia,
)
KYON_KNEE_ACTUATOR_CFG = ActuatorCfg(
  joint_names_expr=["knee_pitch_.*"],
  effort_limit=KNEE_ACTUATOR.effort_limit,
  stiffness=STIFFNESS_KNEE,
  damping=DAMPING_KNEE,
  armature=KNEE_ACTUATOR.reflected_inertia,
)

##
# Keyframes.
##


INIT_STATE = EntityCfg.InitialStateCfg(
  pos=(0.0, 0.0, 0.55),
  joint_pos={
    "hip_roll_1": 0.0,
    "hip_pitch_1": -0.7,
    "knee_pitch_1": 1.4,
    "hip_roll_2": 0.0,
    "hip_pitch_2": 0.7,
    "knee_pitch_2": -1.4,
    "hip_roll_3": 0.0,
    "hip_pitch_3": -0.7,
    "knee_pitch_3": 1.4,
    "hip_roll_4": 0.0,
    "hip_pitch_4": 0.7,
    "knee_pitch_4": -1.4,
  },
  joint_vel={".*": 0.0},
)

##
# Collision config.
##

_foot_regex = r"contact_[1-4]$"

# This disables all collisions except the feet.
# Furthermore, feet self collisions are disabled.
FEET_ONLY_COLLISION = CollisionCfg(
  geom_names_expr=[_foot_regex],
  contype=0,
  conaffinity=1,
  condim=3,
  priority=1,
  friction=(0.6,),
  solimp=(0.9, 0.95, 0.023),
)

# This enables all collisions, excluding self collisions.
# Foot collisions are given custom condim, friction and solimp.
FULL_COLLISION = CollisionCfg(
  geom_names_expr=[".*_collision"],
  condim={_foot_regex: 3, ".*_collision": 1},
  priority={_foot_regex: 1},
  friction={_foot_regex: (0.6,)},
  solimp={_foot_regex: (0.9, 0.95, 0.023)},
  contype=1,
  conaffinity=0,
)

##
# Final config.
##

KYON_ARTICULATION = EntityArticulationInfoCfg(
  actuators=(
    KYON_HIP_ACTUATOR_CFG,
    KYON_KNEE_ACTUATOR_CFG,
  ),
  soft_joint_pos_limit_factor=0.9,
)

KYON_ROBOT_CFG = EntityCfg(
  init_state=INIT_STATE,
  collisions=(FULL_COLLISION,),
  spec_fn=get_spec,
  articulation=KYON_ARTICULATION,
)

KYON_ACTION_SCALE: dict[str, float] = {}
for a in KYON_ARTICULATION.actuators:
  e = a.effort_limit
  s = a.stiffness
  names = a.joint_names_expr
  if not isinstance(e, dict):
    e = {n: e for n in names}
  if not isinstance(s, dict):
    s = {n: s for n in names}
  for n in names:
    if n in e and n in s and s[n]:
      KYON_ACTION_SCALE[n] = 0.5  # rad, for all joints
      
