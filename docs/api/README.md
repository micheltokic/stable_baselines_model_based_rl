<!-- markdownlint-disable -->

# API Overview

## Modules

- [`dynamic_model_trainer`](./dynamic_model_trainer.md#module-dynamic_model_trainer)
- [`dynamic_model_trainer.dynamic_model_trainer`](./dynamic_model_trainer.dynamic_model_trainer.md#module-dynamic_model_trainerdynamic_model_trainer)
- [`dynamic_model_trainer.model_builder`](./dynamic_model_trainer.model_builder.md#module-dynamic_model_trainermodel_builder)
- [`dynamic_model_trainer.tensorflow_data_generator`](./dynamic_model_trainer.tensorflow_data_generator.md#module-dynamic_model_trainertensorflow_data_generator)
- [`dynamic_model_trainer.verifier`](./dynamic_model_trainer.verifier.md#module-dynamic_model_trainerverifier)
- [`sampler`](./sampler.md#module-sampler)
- [`sampler.gym_sampler`](./sampler.gym_sampler.md#module-samplergym_sampler)
- [`utils`](./utils.md#module-utils)
- [`utils.test_functions`](./utils.test_functions.md#module-utilstest_functions)

## Classes

- No classes

## Functions

- [`dynamic_model_trainer.build_and_train_dynamic_model`](./dynamic_model_trainer.dynamic_model_trainer.md#function-build_and_train_dynamic_model): Builds and trains a dynamic model for a given csv dataset retrieved from a gym environment based on configurations
- [`dynamic_model_trainer.sample_environment_and_train_dynamic_model`](./dynamic_model_trainer.dynamic_model_trainer.md#function-sample_environment_and_train_dynamic_model): Sampling data from a given gym environment and building and training a dynamic model for a given csv dataset retrieved from a
- [`model_builder.build_dynamic_model`](./dynamic_model_trainer.model_builder.md#function-build_dynamic_model): Creates and compiles a neural network consisting of a 'Long Short Term Memory' layer followed by a 'Dense' layer.
- [`tensorflow_data_generator.prepare_data`](./dynamic_model_trainer.tensorflow_data_generator.md#function-prepare_data): Reads the data of the data frame,
- [`verifier.evaluate_model`](./dynamic_model_trainer.verifier.md#function-evaluate_model): Measures model quality and displays plotted results on demand
- [`gym_sampler.sample_gym_environment`](./sampler.gym_sampler.md#function-sample_gym_environment): Sample the given gym environment with the given amount of episodes and maximum
- [`test_functions.add_fake_noise`](./utils.test_functions.md#function-add_fake_noise): Returns the dimension of a given gym (action/ observation)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
