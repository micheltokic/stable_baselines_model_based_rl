import os
from copy import deepcopy

import keras
import pandas as pd

from definitions import ROOT_DIR
from stable_baselines_model_based_rl.dynamic_model_trainer import tensorflow_data_generator, model_builder, verifier
from stable_baselines_model_based_rl.utils.configuration import Configuration

import stable_baselines_model_based_rl.sampler.gym_sampler as sampler


def sample_environment_and_train_dynamic_model(gym_environment_name, episode_count, max_steps, output_path):
    """
    Sampling data from a given gym environment and building and training a dynamic model for a given csv dataset retrieved from a
    csv dataset retrieved from a gym environment based on configurations specified in a yaml file.

    Args:
        gym_environment_name: Name of the gym environment from which data is sampled
        episode_count: Number of episodes to be sampled for the dataset
        max_steps: Maximum number of steps in an episode

    Returns:
        lstm_model: The lstm model trained on the given dataset
    """

    data_file_name, config, final_dir_path = sampler.sample_gym_environment(gym_environment_name, episode_count, max_steps, output_path)
    return build_and_train_dynamic_model(data_file_name, config, final_dir_path)


def build_and_train_dynamic_model(data_path, config: Configuration, output_path=ROOT_DIR):
    """
    Builds and trains a dynamic model for a given csv dataset retrieved from a gym environment based on configurations
    specified in a yaml file

    Args:
        data_path: Name of the data file
        config: Configuration Object that contains the given yaml Configuration
        output_path: Directory path of training output

    Returns:
        model: The model trained on the given dataset

    Todo:
    * evaluation, plotting configuration into yaml file?
    """
    data_frame = pd.read_csv(data_path)

    config_dict = deepcopy(config.config)

    print("Configuration dictionary: ", config_dict)

    target_col_names = config.get('input_config.observation_cols')
    action_col_names = config.get('input_config.action_cols')
    input_col_names = action_col_names + target_col_names

    # model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../model_output/model.h5')

    max_epochs = config.get('dynamic_model.training.max_epochs', 100)
    train_test_ration = config.get('dynamic_model.training.train_test_ration', 0.7)
    steps_per_epoch = config.get('dynamic_model.training.steps_per_epoch', 1000)
    validation_steps = config.get('dynamic_model.training.validation_steps', 100)
    validation_freq = config.get('dynamic_model.training.validation_freq', 1)
    optimizer = keras.optimizers.get(config.get('dynamic_model.training.optimizer', 'RMSprop'))
    loss = keras.losses.get(config.get('dynamic_model.training.loss', 'mse'))
    batch_size = config.get('dynamic_model.training.batch_size', 64)
    lag = config.get('dynamic_model.training.lag', 4)
    patience = config.get('dynamic_model.training.patience', 15)
    # optimizer.learning_rate.assign(config.get('dynamic_model.training.learning_rate', 0.1))

    artificial_noise = config.get('dynamic_model.utility_flags.artificial_noise', True)
    noise_settings = {}
    if artificial_noise:
        noise_settings = config.get('dynamic_model.validation.noise')

    train_data, val_data, input_shape, mean_in, std_in, mean_out, std_out = \
        tensorflow_data_generator.prepare_data(data_frame, input_col_names, target_col_names,
                                               window_size=lag,
                                               training_pattern_percent=train_test_ration,
                                               noise_settings=noise_settings)

    callbacks = [keras.callbacks.EarlyStopping(monitor="loss", patience=patience, restore_best_weights=True,
                                               verbose=True)]
    if config.get('dynamic_model.utility_flags.log_training'):
        callbacks.append(keras.callbacks.ModelCheckpoint(filepath=f"{output_path}/model.bestTrainLoss", monitor='loss',
                                                         verbose=1, save_best_only=True, mode=min))
        callbacks.append(keras.callbacks.ModelCheckpoint(filepath=f"{output_path}/bestValLoss", monitor='val_loss',
                                                         verbose=1, save_best_only=True, mode=min))
        callbacks.append(keras.callbacks.TensorBoard(log_dir=".\model_logs_tb", histogram_freq=1))

    print(config.get('dynamic_model.keras_model.config.layers'))
    config.get('dynamic_model.keras_model.config.layers')[0]['batch_input_shape'] = input_shape
    model = model_builder.build_dynamic_model(config.get('dynamic_model.keras_model'), len(target_col_names),
                                              optimizer, loss)

    history = model.fit(train_data, epochs=max_epochs, steps_per_epoch=steps_per_epoch,
                        validation_data=val_data, validation_steps=validation_steps,
                        validation_freq=validation_freq,
                        callbacks=callbacks, batch_size=batch_size)

    model.summary()

    if config.get('dynamic_model.utility_flags.evaluate_model'):
        dfNet, dfEval = verifier.evaluate_model(data_frame, input_col_names, action_col_names, target_col_names,
                                                lag)
        if config.get('dynamic_model.utility_flags.plot_results'):
            fig = verifier.plot_results(input_col_names, action_col_names, dfNet, dfEval, lag, mean_in, std_in)

            if config.get('dynamic_model.utility_flags.save'):
                verifier.save(output_path, model, history.history['val_loss'][len(history.history['val_loss']) - 1],
                              lag, fig, config, data_path)

    return model
