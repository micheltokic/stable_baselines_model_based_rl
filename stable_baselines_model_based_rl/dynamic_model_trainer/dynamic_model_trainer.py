import stable_baselines_model_based_rl.sampler.gym_sampler as sampler
import tensorflow_data_generator
import tensorflow as tf
import model_builder
import pandas as pd
import os
import yaml
import verifier


def sample_environment_and_train_dynamic_model(gym_environment_name, episode_count, max_steps):
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
    return build_and_train_dynamic_model(data_file_name, config_file_name)


def build_and_train_dynamic_model(data_file_name, config_file_name):
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
    * evaluation, plotting configuration into yaml file?
    """
    data_frame = pd.read_csv(data_file_name)

    try:
        with open(config_file_name) as file:
            config_dict = yaml.load(file, Loader=yaml.FullLoader)
    except:
        print("Configuration file could not be loaded")
        return

    print("Configuration dictionary: ", config_dict)

    target_col_names = config_dict['input_config']['observation_cols']
    action_col_names = config_dict['input_config']['action_cols']
    input_col_names = action_col_names + target_col_names

    print("Input Columns: ", input_col_names)
    print("Observation Columns: ", target_col_names)

    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../model_output/model.h5')

    max_epochs = config_dict['dynamic_model']['training']['max_epochs']
    train_test_ration = config_dict['dynamic_model']['training']['train_test_ration']
    steps_per_epoch = config_dict['dynamic_model']['training']['steps_per_epoch']
    validation_steps = config_dict['dynamic_model']['training']['validation_steps']
    validation_freq = config_dict['dynamic_model']['training']['validation_freq']
    optimizer = tf.keras.optimizers.get(config_dict['dynamic_model']['training']['optimizer'])
    loss = tf.keras.losses.get(config_dict['dynamic_model']['training']['loss'])
    batch_size = config_dict['dynamic_model']['training']['batch_size']
    lag = config_dict['dynamic_model']['training']['lag']
    learning_rate = config_dict['dynamic_model']['training']['learning_rate']
    patience = config_dict['dynamic_model']['training']['patience']

    train_data, val_data, input_shape, mean_in, std_in, mean_out, std_out = \
        tensorflow_data_generator.prepare_data(data_frame, input_col_names, target_col_names,
                                               window_size=lag, training_pattern_percent=train_test_ration)

    callbacks = [tf.keras.callbacks.EarlyStopping(monitor="loss", patience=patience, restore_best_weights=True,
                                                  verbose=True)]
    if config_dict['dynamic_model']['utility_flags']['log_training']:
        callbacks.append(tf.keras.callbacks.ModelCheckpoint(filepath="%s.bestTrainLoss" % model_path, monitor='loss',
                                                            verbose=1, save_best_only=True, mode=min))
        callbacks.append(tf.keras.callbacks.ModelCheckpoint(filepath="%s.bestValLoss" % model_path, monitor='val_loss',
                                                            verbose=1, save_best_only=True, mode=min))
        callbacks.append(tf.keras.callbacks.TensorBoard(log_dir=".\model_logs_tb", histogram_freq=1))

    config_dict['dynamic_model']['model']['config']['layers'][0]['batch_input_shape'] = input_shape
    config_dict['dynamic_model']['model']['config']['layers'][
        len(config_dict['dynamic_model']['model']['config']['layers']) - 1]['units'] = len(target_col_names)
    lstm_model = model_builder.build_dynamic_model(config_dict['dynamic_model']['model'], optimizer, loss)
    history = lstm_model.fit(train_data, epochs=max_epochs, steps_per_epoch=steps_per_epoch,
                             validation_data=val_data, validation_steps=validation_steps,
                             validation_freq=validation_freq,
                             callbacks=callbacks)

    if config_dict['dynamic_model']['utility_flags']['export_model']:
        lstm_model.save(model_path)

    if config_dict['dynamic_model']['utility_flags']['evaluate_model']:
        verifier.evaluate_model(data_frame, input_col_names, action_col_names, target_col_names, lag, mean_in, 
            std_in, plot=config_dict['dynamic_model']['utility_flags']['plot_results'])

    return lstm_model
