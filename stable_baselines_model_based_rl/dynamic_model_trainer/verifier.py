import collections
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from stable_baselines_model_based_rl.utils.mean import nested_list_mean


def evaluate_model_with_test_data(model, test_data, input_col_names, action_col_names,
                                  target_col_names, lag):
    """Evaluate the dynamic model with given test data and return average difference per step.
    
    The average (absolute) difference per step is calculated over all episodes of the test data.

    Args:
        model: Dynamic model to use for evaluating predictions.
        test_data: Data frame with test data, not (!) grouped by episode yet.
        input_col_names: Names of the input columns for the model (i.e., action and
            observations/states).
        action_col_names: Names of the action columns.
        target_col_names: Names of the target columns, i.e. state columns (columns predicted by
            the model)
        lag: Used window-size / lag by the model.

    Returns:
        List of average difference per step between prediction and real test data.
    """

    eval_test_data_grouped = test_data.groupby('EPISODE')
    episode_diffs = []

    for group in eval_test_data_grouped:
        eval_test_data = group[1]

        # FIFO-buffer that keeps the neural state
        stateBuffer = collections.deque(maxlen=lag)

        # storage for outputs (predictions) of neural network
        dfNet = pd.DataFrame(data={col_name: [] for col_name in target_col_names})

        for i in range(len(eval_test_data)):
            # estimation of first state
            if i < lag:
                state_data = np.float64([eval_test_data[input_col_names[j]].values[i]
                                        for j in range(len(input_col_names))])
                stateBuffer.append(state_data)
                dfNet = dfNet.append({input_col_names[j]: state_data[j]
                                      for j in range(len(action_col_names), len(input_col_names))},
                                     ignore_index=True)

            # predict successor state
            else:
                # recall of neural network
                state = np.array([list(stateBuffer)])
                netOutput = model.predict(np.float64(state))[0]

                # append plotting data
                dfNet = dfNet.append({target_col_names[j]: netOutput[j]
                                    for j in range(len(target_col_names))}, ignore_index=True)

                # update RNN state
                dfEval_actions = np.float64([eval_test_data[action_col_name].values[i]
                                            for action_col_name in action_col_names])
                stateBuffer.append(np.concatenate((dfEval_actions, netOutput)))

        # Calculate summed absolute difference/ deviation between prediction and real test
        # data over all observation columns.
        dfDiff = (eval_test_data[target_col_names].reset_index(drop=True) - dfNet).abs()
        dfSum = dfDiff.sum(axis=1)
        episode_diffs.append(list(dfSum))
    
    # average the absolute differences over all test episodes
    return nested_list_mean(episode_diffs)


def evaluate_model(model, data_frame, input_col_names, action_col_names, target_col_names, lag):
    """
    Evaluate a given model against the longest episode of the given data_frame.

    Args:
        model: Model
        data_frame: Data
        input_col_names: Names of the inputs
        action_col_names: Names of the action inputs
        target_col_names: Names of the targets
        lag: Number of past time steps that are taken into account

    Returns:
        dfNet: Predictions of the model.
        dfEval: DataFrame containing the longest episode of the given data_frame. This is the
            episode the model was evaluated against.
    """

    row_max_steps = data_frame.loc[data_frame['STEP'].idxmax()]
    dfEval = data_frame[data_frame.EPISODE == row_max_steps.EPISODE]

    # FIFO-buffer that keeps the neural state
    stateBuffer = collections.deque(maxlen=lag)

    # outputs of neural network will be stored here
    d = {"EPISODE": [], "STEP": []}
    d.update({col_name: [] for col_name in input_col_names})
    dfNet = pd.DataFrame(data=d)

    len_dfEval = len(dfEval)
    for i in range(0, len_dfEval):

        # estimation of first state
        if i < lag:
            state_data = np.float64(
                [dfEval[input_col_names[j]].values[i] for j in range(0, len(input_col_names))])
            stateBuffer.append(state_data)

        # predict successor state
        else:
            # recall of neural network
            state = np.array([list(stateBuffer)])
            if i == lag:
                print(state)
            netOutput = model.predict(np.float64(state))[0]

            # append plotting data
            dfNet = dfNet.append(
                {target_col_names[j]: netOutput[j] for j in range(0, len(target_col_names))},
                ignore_index=True)

            # update RNN state
            dfEval_actions = np.float64(
                [dfEval[action_col_name].values[i] for action_col_name in action_col_names])
            stateBuffer.append(np.concatenate((dfEval_actions, netOutput)))

    return dfNet, dfEval


def plot_results(target_col_names, action_col_names, dfNet, dfEval, dfDiff, window_size):
    """Create a evaluation plot for given data."""

    # the two for additional plots 1. std and 2. for overall training deviation
    plot_count = len(target_col_names) + 2
    fig, axs = plt.subplots(plot_count, 1, figsize=(10, plot_count * 5))

    for action in action_col_names:
        axs[0].plot(range(len(dfNet)), dfEval[action].values[window_size:],
                    label=action)
    axs[0].grid()
    axs[0].legend(loc="best")

    for i in range(len(target_col_names)):
        col_name = target_col_names[i]
        axs[i+1].plot(range(len(dfNet)), dfEval[col_name].values[window_size:], label=col_name)

        axs[i+1].plot(range(len(dfNet)), dfNet[col_name].values, label="prediction", ls="--")

        axs[i+1].grid()
        axs[i+1].legend(loc="best")

    # plot std & mean
    axs[plot_count-1].plot(range(len(dfDiff)), dfDiff, label='absolute deviation from training')
    axs[plot_count-1].grid()
    axs[plot_count-1].legend(loc="best")

    return fig


def save(final_dir_path, model, fig, config, df, debug):
    """Save given data to given final_dir_path.

    In debug mode, the config file and the df (DataFram = data) are stored, additionally.

    Args:
        final_dir_path: Output directory to store the data to.
        model: Keras Model to export (It'll be only exported, if the corresponding config setting
            ("dynamic_model.utility_flags.export_model") is set to True).
        fig: Figure to export (optionally, otherwise None).
        config: Configuration.
        df: DataFrame containing the data the model was created with
        debug: Debug Flag: controlls whether df and config are addtionally exported.
    """

    # store input data in debug mode in model output folder as well
    if debug:
        df.to_csv(os.path.join(final_dir_path, 'data.csv'), sep=',', encoding='utf-8', index=False)
        config.save_config(file=os.path.join(final_dir_path, 'config.yaml'))

    model_path = f'{final_dir_path}/model.h5'
    if config.get('dynamic_model.utility_flags.export_model'):
        model.save(model_path)

    fig_path = None
    if fig is not None:
        fig_path = f'{final_dir_path}/plot.png'
        fig.savefig(fig_path)

    return model_path, fig_path
