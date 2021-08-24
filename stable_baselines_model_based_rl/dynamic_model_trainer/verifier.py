import collections
import tensorflow as tf
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime
from shutil import copyfile, copy2

from definitions import ROOT_DIR


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
    * fix plotting error: ValueError: x and y must have same first dimension, but have shapes (0,) and (64,)
    * plot actions for different action spaces
    """

    row_max_steps = data_frame.loc[data_frame['STEP'].idxmax()]
    print(row_max_steps)

    dfEval = data_frame[data_frame.EPISODE == row_max_steps.EPISODE]
    dfEval.describe()

    # model_output_path = os.path.join(ROOT_DIR, '../../model_output/')
    # model = tf.keras.models.load_model(f"{model_output_path}model.h5.bestValLoss", compile=False)

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
            state_data = np.float64([dfEval[input_col_names[j]].values[i] for j in range(0, len(input_col_names))])

            # state_data = np.float64([dfEval[CART_POS].values[i], dfEval[CART_VEL].values[i],
            #                         dfEval[PEND_POS].values[i], dfEval[PEND_VEL].values[i],
            #                         dfEval[ACTION].values[i]])

            stateBuffer.append(state_data)
            # print ("Filling initState: %s" % state_data)

        # predict successor state
        else:

            # recall of neural network
            state = np.array([list(stateBuffer)])
            if i == lag:
                print(state)
            netOutput = model.predict(np.float64(state))[0]

            # append plotting data
            dfNet = dfNet.append({target_col_names[j]: netOutput[j] for j in range(0, len(target_col_names))}
                                 , ignore_index=True)

            # update RNN state
            dfEval_actions = np.float64([dfEval[action_col_name].values[i] for action_col_name in action_col_names])
            stateBuffer.append(np.concatenate((dfEval_actions, netOutput)))

    return dfNet, dfEval


def plot_results(input_col_names, action_col_names, dfNet, dfEval, window_size, mean, std):
    now_str = datetime.now().strftime("%d%m%Y-%H%M%S")
    fig, axs = plt.subplots(len(input_col_names) + 1, 1, figsize=(10, 15))

    # TODO
    for i in range(len(input_col_names)):
        col_name = input_col_names[i]
        axs[i].plot(range(len(dfNet)), dfEval[col_name].values[window_size:], label=col_name)

        if col_name not in action_col_names:
            axs[i].plot(range(len(dfNet)), dfNet[col_name].values, label="prediction", ls="--")

        axs[i].grid()
        axs[i].legend(loc="best")

    # plot std & mean
    axs[len(input_col_names)].errorbar(range(len(mean)), mean, std, linestyle='None', marker='^')

    plt.show()

    return fig


def save(final_dir_path, model, loss, lag, fig, config, df):
    df.to_csv(os.path.join(final_dir_path, 'data.csv'), sep=',', encoding='utf-8', index=False)
    config.save_config(file=os.path.join(final_dir_path, "config.yaml"))

    if config.get('dynamic_model.utility_flags.export_model'):
        model.save(f'{final_dir_path}/model.h5')

    fig.savefig(f'{final_dir_path}/plot.png')

    root_path, _, last_folder_name = final_dir_path.rpartition(os.path.sep)
    rounded_lag = "{:.2f}".format(round(lag, 4))
    new_folder_name = f'loss={loss}-lag={rounded_lag}-{last_folder_name}'
    new_dir_path = os.path.join(root_path, new_folder_name)
    try:
        os.rename(final_dir_path, new_dir_path)
        final_dir_path = new_dir_path
    except PermissionError:
        print(f'Permission Error: folder {final_dir_path} could not be renamed to {final_dir_path}')

    print(f"Training and model saved to {final_dir_path}")
