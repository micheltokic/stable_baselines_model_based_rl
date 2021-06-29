from setuptools import setup

setup(name='coloring',
      version='0.0.1',
      # for visualization also install matplotlib
      install_requires=['gym', 'stable-baselines3[extra]']
      )
