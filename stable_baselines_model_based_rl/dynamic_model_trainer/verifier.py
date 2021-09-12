import collections
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def evaluate_model_with_test_data(model, test_data, input_col_names, action_col_names, target_col_names):
    eval_test_data = test_data.copy()
    eval_test_data.describe()

    # FIFO-buffer that keeps the neural state
    stateBuffer = collections.deque()

    # outputs of neural network will be stored here
    d = {"EPISODE": [], "STEP": []}
    d.update({col_name: [] for col_name in input_col_names})
    dfNet = pd.DataFrame(data=d) # holds predictions

    len_test_data = len(test_data)
    for i in range(0, len_test_data):

        # estimation of first state
        if i == 0:
            state_data = np.float64([eval_test_data[input_col_names[j]].values[i] for j in range(0, len(input_col_names))])
            stateBuffer.append(state_data)
        
        # predict successor state
        else:

            # recall of neural network
            state = np.array([list(stateBuffer)])
            netOutput = model.predict(np.float64(state))[0]

            # append plotting data
            dfNet = dfNet.append({target_col_names[j]: netOutput[j] for j in range(0, len(target_col_names))}
                                 , ignore_index=True)

            # update RNN state
            dfEval_actions = np.float64([eval_test_data[action_col_name].values[i] for action_col_name in action_col_names])
            stateBuffer.append(np.concatenate((dfEval_actions, netOutput)))

    # first normalize all observation data for comparisons later on
    normed_target_df = (test_data[target_col_names]-test_data[target_col_names].mean())/test_data[target_col_names].std()
    normed_target_df = normed_target_df.iloc[1:, :].reset_index(drop=True)
    # calculate mean diff between normed obs data and prediction for comparison later
    dfDiff = (normed_target_df - dfNet[target_col_names]).abs()
    dfSum = dfDiff.sum(axis=1) # sum all columns into one
    dfMean = dfSum.div(len(target_col_names), axis=0) # divide all row entries by obs
    
    return dfMean


def evaluate_model(model, data_frame, input_col_names, action_col_names, target_col_names, lag):
    """
    Measures model quality and displays plotted results on demand

    Args:
        model: Model
        data_frame: Data
        input_col_names: Names of the inputs
        action_col_names: Names of the action inputs
        target_col_names: Names of the targets
        lag: Number of past time steps that are taken into account

    Todo:
        fix plotting error: ValueError: x and y must have same first dimension, but
            have shapes (0,) and (64,)
        plot actions for different action spaces
    """

    row_max_steps = data_frame.loc[data_frame['STEP'].idxmax()]
    print(row_max_steps)

    dfEval = data_frame[data_frame.EPISODE == row_max_steps.EPISODE]
    dfEval.describe()

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


def plot_results(input_col_names, action_col_names, dfNet, dfEval, dfDiff,
                 window_size, mean, std, debug):
    # the two for additional plots 1. std and 2. for overall training deviation
    plot_count = len(input_col_names) + 2
    fig, axs = plt.subplots(plot_count, 1, figsize=(10, 20))

    for i in range(len(input_col_names)):
        col_name = input_col_names[i]
        axs[i].plot(range(len(dfNet)), dfEval[col_name].values[window_size:], label=col_name)

        if col_name not in action_col_names:
            axs[i].plot(range(len(dfNet)), dfNet[col_name].values, label="prediction", ls="--")

        axs[i].grid()
        axs[i].legend(loc="best")

    # plot std & mean
    axs[len(input_col_names)].plot(range(len(dfDiff)), dfDiff.values,
                                   label='absolute deviation from training')
    axs[len(input_col_names)+1].errorbar(range(len(mean)), mean, std, linestyle='None', marker='^')
    
    if debug:
        plt.show()

    return fig


def save(final_dir_path, model, fig, config, df, debug):
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
