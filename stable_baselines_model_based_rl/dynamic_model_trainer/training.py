import os
from datetime import datetime

import keras
import pandas as pd

from definitions import ROOT_DIR
from stable_baselines_model_based_rl.dynamic_model_trainer import prepare_data, model_builder, verifier
from stable_baselines_model_based_rl.utils.configuration import Configuration

import stable_baselines_model_based_rl.sampler.gym_sampler as sampler


def build_and_train_dynamic_model(data_path, config: Configuration, output_path=ROOT_DIR,
                                  debug: bool = False):
    """
    Builds and trains a dynamic model for a given csv dataset retrieved from a gym environment
    based on configurations specified in a yaml file

    Args:
        data_path: Name of the data file
        config: Configuration Object that contains the given yaml Configuration
        output_path: Directory path of training output
        debug: Flag to enable additional debug features, such as renaming the directory of the
            resulting model based on the used lag value and the resulted loss.

    Returns:
        model: The model trained on the given dataset
        output_path: The path were everything has been stored
        model_file_path: The path to the exported model file (None, if it shouldn't be exported)

    Todo:
        evaluation, plotting configuration into yaml file?
    """
    df = pd.read_csv(data_path)
    return __build_and_train_dynamic_model(df, config, output_path, debug)


def __build_and_train_dynamic_model(df: pd.DataFrame, config: Configuration, path=ROOT_DIR,
                                    debug: bool = False):
    target_col_names = config.get('input_config.observation_cols')
    action_col_names = config.get('input_config.action_cols')
    input_col_names = action_col_names + target_col_names
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

    artificial_noise = config.get('dynamic_model.utility_flags.artificial_noise', False)
    noise_settings = config.get('dynamic_model.validation.noise') if artificial_noise else {}

    path = os.path.join(path, 'dynamic_models')
    final_dir_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    output_path = os.path.join(path, final_dir_name)
    os.makedirs(output_path, exist_ok=True)

    train_data, val_data, test_data, input_shape, mean_in, std_in, mean_out, std_out = \
        prepare_data.prepare_data(df, input_col_names, target_col_names,
                                  window_size=lag,
                                  training_pattern_percent=train_test_ration,
                                  noise_settings=noise_settings, config=config)

    callbacks = [keras.callbacks.EarlyStopping(monitor="loss", patience=patience,
                                               restore_best_weights=True, verbose=True)]
    if config.get('dynamic_model.utility_flags.log_training'):
        callbacks.append(
            keras.callbacks.ModelCheckpoint(filepath=f"{output_path}/model.bestTrainLoss",
                                            monitor='loss', verbose=1, save_best_only=True,
                                            mode=min))
        callbacks.append(
            keras.callbacks.ModelCheckpoint(filepath=f'{output_path}/model.bestValLoss',
                                            monitor='val_loss', verbose=1, save_best_only=True,
                                            mode=min))
        callbacks.append(
            keras.callbacks.TensorBoard(log_dir=f'{output_path}/model.tensorboard_logs',
                                        histogram_freq=1))

    model = model_builder.build_dynamic_model(config.get('dynamic_model.keras_model'), input_shape,
                                              mean_in, std_in, mean_out, std_out,
                                              len(target_col_names), optimizer, loss)

    history = model.fit(train_data, epochs=max_epochs, steps_per_epoch=steps_per_epoch,
                        validation_data=val_data, validation_steps=validation_steps,
                        validation_freq=validation_freq,
                        callbacks=callbacks, batch_size=batch_size)

    model.summary()

    fig = None
    if config.get('dynamic_model.utility_flags.evaluate_model'):
        dfNet, dfEval = verifier.evaluate_model(model, df, input_col_names, action_col_names,
                                                target_col_names, lag)
        dfDiff = verifier.evaluate_model_with_test_data(model, test_data, input_col_names,
                                                        action_col_names, target_col_names, lag)
        if config.get('dynamic_model.utility_flags.plot_results'):
            fig = verifier.plot_results(target_col_names, action_col_names, dfNet, dfEval,
                                        dfDiff, lag, mean_in, std_in, debug)
    model_file_path = None
    if config.get('dynamic_model.utility_flags.save'):
        model_file_path, _ = verifier.save(output_path, model, fig, config, df, debug)
    
    if debug:
        rounded_lag = "{:.2f}".format(round(lag, 4))
        last_loss = history.history['val_loss'][len(history.history['val_loss']) - 1]
        new_folder_name = f'{final_dir_name}_loss={last_loss}_lag={rounded_lag}'
        new_dir_path = os.path.join(path, new_folder_name)
        try:
            os.rename(output_path, new_dir_path)
            output_path = new_dir_path
        except PermissionError:
            print(f'Permission Error: folder {output_path} could not be renamed'
                  f'to {new_dir_path}')
    
    print(f'Output saved to: {output_path}')
    return model, output_path, model_file_path
