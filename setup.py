from setuptools import find_packages, setup

setup(
    name='stable_baselines_model_based_rl',
    version='0.0.1',
    packages=find_packages(),
    requires=['setuptools'],
    install_requires=[
        'gym==0.18.3',
        'numpy==1.19.3',
        'pandas==1.2.5',
        'PyYAML==5.4.1',
        'stable-baselines3[extra]==1.0',
        'tensorflow~=2.5.0',
        'matplotlib~=3.4.2',
        'click~=7.1.2',
    ],
    entry_points={
        'console_scripts': [
            'sb-mbrl = stable_baselines_model_based_rl.cli.sb_mbrl:sb_mbrl',
            'sb-mbrl-eval = stable_baselines_model_based_rl.cli.sb_mbrl_eval:evaluate_sb_policy_against_gym_env',
            'sb-mbrl-obtain-config-file = stable_baselines_model_based_rl.cli.sb_mbrl_obtain_config_file:obtain_config_file',
        ],
    },
)
