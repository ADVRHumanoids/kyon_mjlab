import gymnasium as gym

gym.register(
  id="Mjlab-Velocity-Flat-Iit-Kyon",
  entry_point="mjlab.envs:ManagerBasedRlEnv",
  disable_env_checker=True,
  kwargs={
    "env_cfg_entry_point": f"{__name__}.flat_env_cfg:IitKyonFlatEnvCfg",
    "rl_cfg_entry_point": f"{__name__}.rl_cfg:IitKyonPPORunnerCfg",
  },
)

gym.register(
  id="Mjlab-Velocity-Flat-Iit-Kyon-Play",
  entry_point="mjlab.envs:ManagerBasedRlEnv",
  disable_env_checker=True,
  kwargs={
    "env_cfg_entry_point": f"{__name__}.flat_env_cfg:IitKyonFlatEnvCfg_PLAY",
    "rl_cfg_entry_point": f"{__name__}.rl_cfg:IitKyonPPORunnerCfg",
  },
)

print("[INFO] Registered Mjlab-Velocity-Flat-Iit-Kyon environment.")
print("[INFO] Registered Mjlab-Velocity-Flat-Iit-Kyon-Play environment.")