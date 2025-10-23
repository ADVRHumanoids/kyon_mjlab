from dataclasses import dataclass, replace

from kyon_mjlab.assets.robots.kyon.kyon_config import (
  KYON_ACTION_SCALE,
  KYON_ROBOT_CFG,
)
from kyon_mjlab.tasks.velocity.velocity_env_cfg import (
  LocomotionVelocityEnvCfg,
)
from mjlab.utils.spec_config import ContactSensorCfg


@dataclass
class IitKyonRoughEnvCfg(LocomotionVelocityEnvCfg):
  def __post_init__(self):
    super().__post_init__()
    
    foot_names = ["FL", "FR", "RL", "RR"]
    sensor_names = [f"{name}_foot_ground_contact" for name in foot_names]
    geom_names = [f"contact_{id+1}" for id in range(4)]

    foot_contact_sensors = [
      ContactSensorCfg(
        name=sensor_name,
        geom1=geom_name,
        body2="terrain",
        num=1,
        data=("found",),
        reduce="netforce",
      )
      for sensor_name, geom_name in zip(sensor_names, geom_names)
    ]
          
    kyon_cfg = replace(KYON_ROBOT_CFG, sensors=tuple(foot_contact_sensors))
    self.scene.entities = {"robot": kyon_cfg}

    self.actions.joint_pos.scale = KYON_ACTION_SCALE

    self.rewards.air_time.params["sensor_names"] = sensor_names
    self.rewards.pose.params["std"] = {
      r"hip_roll_.*": 0.3,
      r"hip_pitch_.*": 0.3,
      r"knee_pitch_.*": 0.6,
    }

    self.events.foot_friction.params["asset_cfg"].geom_names = geom_names

    self.observations.critic.contacts.params["sensor_names"] = sensor_names

    self.viewer.body_name = "base_link"
    self.viewer.distance = 1.5
    self.viewer.elevation = -10.0


@dataclass
class IitKyonRoughEnvCfg_PLAY(IitKyonRoughEnvCfg):
  def __post_init__(self):
    super().__post_init__()

    # Effectively infinite episode length.
    self.episode_length_s = int(1e9)

    if self.scene.terrain is not None:
      if self.scene.terrain.terrain_generator is not None:
        self.scene.terrain.terrain_generator.curriculum = False
        self.scene.terrain.terrain_generator.num_cols = 5
        self.scene.terrain.terrain_generator.num_rows = 5
        self.scene.terrain.terrain_generator.border_width = 10.0

    self.curriculum.command_vel = None
    self.commands.twist.ranges.lin_vel_x = (-1.0, 1.0)
    self.commands.twist.ranges.ang_vel_z = (-1.0, 1.0)
