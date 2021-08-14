<!-- markdownlint-disable -->

# API Overview

## Modules

- [`dynamic_model_trainer`](./dynamic_model_trainer.md#module-dynamic_model_trainer)
- [`dynamic_model_trainer.model_builder`](./dynamic_model_trainer.model_builder.md#module-dynamic_model_trainermodel_builder)
- [`dynamic_model_trainer.tensorflow_data_generator`](./dynamic_model_trainer.tensorflow_data_generator.md#module-dynamic_model_trainertensorflow_data_generator)
- [`dynamic_model_trainer.training`](./dynamic_model_trainer.training.md#module-dynamic_model_trainertraining)
- [`dynamic_model_trainer.verifier`](./dynamic_model_trainer.verifier.md#module-dynamic_model_trainerverifier)
- [`sampler`](./sampler.md#module-sampler)
- [`sampler.gym_sampler`](./sampler.gym_sampler.md#module-samplergym_sampler)
- [`utils`](./utils.md#module-utils)
- [`utils.configuration`](./utils.configuration.md#module-utilsconfiguration)
- [`utils.noise`](./utils.noise.md#module-utilsnoise)
- [`utils.spaces`](./utils.spaces.md#module-utilsspaces)
- [`utils.spaces.base`](./utils.spaces.base.md#module-utilsspacesbase)
- [`utils.spaces.box`](./utils.spaces.box.md#module-utilsspacesbox)
- [`utils.spaces.discrete`](./utils.spaces.discrete.md#module-utilsspacesdiscrete)
- [`utils.spaces.factory`](./utils.spaces.factory.md#module-utilsspacesfactory)
- [`wrapper`](./wrapper.md#module-wrapper)
- [`wrapper.step_handler`](./wrapper.step_handler.md#module-wrapperstep_handler)
- [`wrapper.wrapped_model_env`](./wrapper.wrapped_model_env.md#module-wrapperwrapped_model_env)

## Classes

- [`configuration.Configuration`](./utils.configuration.md#class-configuration): Utility class for loading, accessing and modifying the configuration file for this framework.
- [`base.SpaceType`](./utils.spaces.base.md#class-spacetype): An enumeration.
- [`base.SpaceValue`](./utils.spaces.base.md#class-spacevalue): A SpaceValue represents a wrapper for a given gym space (like Box, or Discrete) and concrete
- [`box.BoxSpaceValue`](./utils.spaces.box.md#class-boxspacevalue)
- [`discrete.DiscreteSpaceValue`](./utils.spaces.discrete.md#class-discretespacevalue)
- [`step_handler.StepRewardDoneHandler`](./wrapper.step_handler.md#class-steprewarddonehandler): The reward handler is responsible for calculating the reward for the current state and the
- [`wrapped_model_env.WrappedModelEnv`](./wrapper.wrapped_model_env.md#class-wrappedmodelenv): This class wraps a dynamic model (created with the stable_baselines_model_based_rl library) as

## Functions

- [`model_builder.build_dynamic_model`](./dynamic_model_trainer.model_builder.md#function-build_dynamic_model): Creates and compiles a neural network consisting of a 'Long Short Term Memory' layer followed by a 'Dense' layer.
- [`tensorflow_data_generator.prepare_data`](./dynamic_model_trainer.tensorflow_data_generator.md#function-prepare_data): Reads the data of the data frame,
- [`training.build_and_train_dynamic_model`](./dynamic_model_trainer.training.md#function-build_and_train_dynamic_model): Builds and trains a dynamic model for a given csv dataset retrieved from a gym environment based on configurations
- [`training.sample_environment_and_train_dynamic_model`](./dynamic_model_trainer.training.md#function-sample_environment_and_train_dynamic_model): Sampling data from a given gym environment and building and training a dynamic model for a given csv dataset retrieved from a
- [`verifier.evaluate_model`](./dynamic_model_trainer.verifier.md#function-evaluate_model): Measures model quality and displays plotted results on demand
- [`verifier.plot_results`](./dynamic_model_trainer.verifier.md#function-plot_results)
- [`verifier.save`](./dynamic_model_trainer.verifier.md#function-save)
- [`gym_sampler.sample_gym_environment`](./sampler.gym_sampler.md#function-sample_gym_environment): Sample the given gym environment with the given amount of episodes and maximum
- [`noise.add_fake_noise`](./utils.noise.md#function-add_fake_noise): Returns the dimension of a given gym (action/ observation)
- [`noise.add_gaussian_noise`](./utils.noise.md#function-add_gaussian_noise)
- [`base.generate_gym_box_space`](./utils.spaces.base.md#function-generate_gym_box_space): Create a gym box space and derive parameters from given arguments. Either a dimension
- [`factory.space_value_from_gym`](./utils.spaces.factory.md#function-space_value_from_gym): Create a SpaceValue instance from the given gym-space "type", the respective value and the type


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
