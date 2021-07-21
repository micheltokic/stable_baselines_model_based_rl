import stable_baselines_model_based_rl.sampler.gym_sampler as sampler
import tensorflow_data_generator
import tensorflow as tf
import model_builder
import pandas as pd
import os
import yaml
import verifier


def sample_environment_and_train_dynamic_model(gym_environment_name, episode_count, max_steps, log=True,
                                               evaluate_model=True, plot_results=True, export_model=True):
    """
    Sampling data from a given gym environment and building and training a dynamic model for a given csv dataset retrieved from a
    csv dataset retrieved from a gym environment based on configurations specified in a yaml file.

    Args:
        gym_environment_name: Name of the gym environment from which data is sampled
        episode_count: Number of episodes to be sampled for the dataset
        max_steps: Maximum number of steps in an episode
        log: Specifies whether logging is desired
        evaluate_model: Specifies whether the evaluation of the model is desired
        plot_results: Specifies whether plotting is desired
        export_model: Specifies whether the export of the model is desired

    Returns:
        lstm_model: The lstm model trained on the given dataset
    """
    data_file_name, config_file_name = sampler.sample_gym_environment(gym_environment_name, episode_count, max_steps)
    return build_and_train_dynamic_model(data_file_name, config_file_name, log=log, evaluate_model=evaluate_model,
                                         plot_results=plot_results, export_model=export_model)


def build_and_train_dynamic_model(data_file_name, config_file_name, log=True, evaluate_model=True, plot_results=True,
                                  export_model=True):
    """
    Builds and trains a dynamic model for a given csv dataset retrieved from a gym environment based on configurations
    specified in a yaml file

    Args:
        data_file_name: Shape of the input
        config_file_name: Mean of the targets to determine dense layer length
        log: Specifies whether logging is desired
        evaluate_model: Specifies whether the evaluation of the model is desired
        plot_results: Specifies whether plotting is desired
        export_model: Specifies whether the export of the model is desired

    Returns:
        lstm_model: The lstm model trained on the given dataset

    Todo:
    * training configuration into yaml file? patience, window_size, max_epochs, steps_per_epoch, validation_steps,
    validation_frequency, ...
    * model configuration into yaml file? number_of_layers, type_of_layers, neurons_per_layer, ...
    * evaluation, plotting configuration into yaml file?
    """
    data_frame = pd.read_csv(data_file_name)
    with open(config_file_name) as file:
        config_dict = yaml.load(file, Loader=yaml.FullLoader)

    print("Configuration Dictionary: ", config_dict)

    input_col_names = config_dict['action_cols'] + config_dict['observation_cols']
    target_col_names = config_dict['observation_cols']

    print("Input Columns: ", input_col_names)
    print("Observation Columns: ", target_col_names)

    # 4 steps into the past... Why ? window_size == lag ?
    window_size = int(config_dict["lags"])

    train_data, val_data, input_shape, mean_in, std_in, mean_out, std_out = \
        tensorflow_data_generator.prepare_data(data_frame, input_col_names, target_col_names,
                                               window_size=window_size, training_pattern_percent=0.7)

    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../model_output/model.h5')
    max_epochs = 1
    steps_per_epoch = 100
    validation_steps = 100
    validation_freq = 1

    callbacks = [tf.keras.callbacks.EarlyStopping(monitor="loss", patience=50, restore_best_weights=True,
                                                  verbose=True)]

    if log:
        callbacks.append(tf.keras.callbacks.ModelCheckpoint(filepath="%s.bestTrainLoss" % model_path, monitor='loss',
                                                            verbose=1, save_best_only=True, mode=min))
        callbacks.append(tf.keras.callbacks.ModelCheckpoint(filepath="%s.bestValLoss" % model_path, monitor='val_loss',
                                                            verbose=1, save_best_only=True, mode=min))
        callbacks.append(tf.keras.callbacks.TensorBoard(log_dir=".\model_logs_tb", histogram_freq=1))

    lstm_model = model_builder.build_lstm(input_shape, mean_out)
    history = lstm_model.fit(train_data, epochs=max_epochs, steps_per_epoch=steps_per_epoch,
                             validation_data=val_data, validation_steps=validation_steps,
                             validation_freq=validation_freq,
                             callbacks=callbacks)

    if export_model:
        lstm_model.save(model_path)

    if evaluate_model:
        verifier.evaluate_model(data_frame, input_col_names, config_dict['action_cols'], target_col_names, window_size, plot=plot_results)

    return lstm_model
