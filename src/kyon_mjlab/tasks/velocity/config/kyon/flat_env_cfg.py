from dataclasses import dataclass

from kyon_mjlab.tasks.velocity.config.kyon.rough_env_cfg import (
  IitKyonRoughEnvCfg,
)


@dataclass
class IitKyonFlatEnvCfg(IitKyonRoughEnvCfg):
  def __post_init__(self):
    super().__post_init__()

    assert self.scene.terrain is not None
    self.scene.terrain.terrain_type = "plane"
    self.scene.terrain.terrain_generator = None
    self.curriculum.terrain_levels = None


@dataclass
class IitKyonFlatEnvCfg_PLAY(IitKyonFlatEnvCfg):
  def __post_init__(self):
    super().__post_init__()

    # Effectively infinite episode length.
    self.episode_length_s = int(1e9)

    self.curriculum.command_vel = None
    self.commands.twist.ranges.lin_vel_x = (-1.0, 1.0)
    self.commands.twist.ranges.ang_vel_z = (-1.0, 1.0)
