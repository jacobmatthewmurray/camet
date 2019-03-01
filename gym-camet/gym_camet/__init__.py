from gym.envs.registration import register

register(
    id='Camet-v0',
    entry_point='gym_camet.envs:CametEnv',
)

register(
    id='Camet-Dual-v0',
    entry_point='gym_camet.envs:CametDualEnv',
)
