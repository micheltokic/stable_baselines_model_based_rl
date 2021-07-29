from setuptools import find_packages, setup

setup(
    name='stable_baselines_model_based_rl',
    version='0.0.1',
    packages=find_packages(
        where='stable_baselines_model_based_rl',
    ),
    package_dir={'': 'stable_baselines_model_based_rl'},
    requires=['setuptools'],
    install_requires=[
        'gym==0.18.3',
        'numpy==1.19.3',
        'pandas==1.2.5',
        'PyYAML==5.4.1',
        'stable-baselines3[extra]==1.0',
        'tensorflow~=2.5.0',
        'matplotlib~=3.4.2',
    ],
)
