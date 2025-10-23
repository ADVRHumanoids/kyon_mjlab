from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

import torch

from mjlab.entity import Entity
from mjlab.managers.scene_entity_config import SceneEntityCfg
from mjlab.third_party.isaaclab.isaaclab.utils.math import quat_error_magnitude

if TYPE_CHECKING:
  from mjlab.envs import ManagerBasedRlEnv

_DEFAULT_ASSET_CFG = SceneEntityCfg("robot")

def contact_found(
  env: ManagerBasedRlEnv,
  sensor_names: list[str],
  asset_cfg: SceneEntityCfg = _DEFAULT_ASSET_CFG,
) -> torch.Tensor:
  """Cost that returns the number of self-collisions detected by a sensor."""
  asset: Entity = env.scene[asset_cfg.name]
  for sensor_name in sensor_names:
    if sensor_name not in asset.sensor_names:
        raise ValueError(
            f"Sensor '{sensor_name}' not found in asset '{asset_cfg.name}'. "
            f"Available sensors: {asset.sensor_names}"
            )
  # Contact sensor is configured to return max_contacts slots, where the size of each
  # slot is determined by the `data` field in the sensor config.
  # With data='found' and reduce='netforce', only the first slot will be positive
  # if there is any contact and the value will be the number of contacts detected, up
  # to max_contacts.
  # See https://mujoco.readthedocs.io/en/latest/XMLreference.html#sensor-contact for
  # more details.
  
  # concatenate contact data from all sensors
  contact_data = torch.cat(
      [asset.data.sensor_data[sensor_name] for sensor_name in sensor_names],
        dim=-1,
  )
  
  return contact_data  # (num_envs, num_sensors)
