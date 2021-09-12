# Home / Introduction

A Model-Based Reinforcement Learning Extension for Stable Baselines.

## Overview
This library provides separate components/ building blocks for four
distinct tasks, namely:

- **Sampling Data from a Gym Environement**. This step may be not required, if
  you already have data you want to use to train a dynamic model with.
- **Train a dynamic Model**. Either use sampled data from previous step, or your
  own data to train a dynamic model.
- **Wrap dynamic model in Gym Environment**. The framework can wrap the trained
  model in a gym environemtn with proper action and oberservation space. You
  only need to define a few details about your input data 
- **Train Policy with Stable Baselines**. Use any stable baselines algorithm to
  to train a poliy against the wrapped gym environment. You only have to specify
  some kind of reward function.

Depending on your use-case, you may only use some specific parts of the library.
