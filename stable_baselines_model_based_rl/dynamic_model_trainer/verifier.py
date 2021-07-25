import collections
import tensorflow as tf
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime


def evaluate_model(data_frame, input_col_names, action_col_names, target_col_names, window_size, mean, std, plot=True):
    """
    Measures model quality and displays plotted results on demand

    Args:
        data_frame: Data
        input_col_names: Names of the inputs
        action_col_names: Names of the action inputs
        target_col_names: Names of the targets
        window_size: Number of past time steps that are taken into account
        plot: Specifies whether plotting is desired

    Todo:
    * fix plotting error: ValueError: x and y must have same first dimension, but have shapes (0,) and (64,)
    * plot actions for different action spaces
    """

    row_max_steps = data_frame.loc[data_frame['STEP'].idxmax()]
    print(row_max_steps)

    dfEval = data_frame[data_frame.EPISODE == row_max_steps.EPISODE]
    dfEval.describe()

    model_output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../model_output/')
    model = tf.keras.models.load_model(f"{model_output_path}model.h5.bestValLoss", compile=False)

    # FIFO-buffer that keeps the neural state
    stateBuffer = collections.deque(maxlen=window_size)

    # outputs of neural network will be stored here
    d = {"EPISODE": [], "STEP": []}
    d.update({col_name: [] for col_name in input_col_names})
    dfNet = pd.DataFrame(data=d)

    len_dfEval = len(dfEval)
    for i in range(0, len_dfEval):

        # estimation of first state
        if i < window_size:
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
            if i == window_size:
                print(state)
            netOutput = model.predict(np.float64(state))[0]

            # append plotting data
            dfNet = dfNet.append({target_col_names[j]: netOutput[j] for j in range(0, len(target_col_names))}
                                 , ignore_index=True)

            # update RNN state
            dfEval_actions = np.float64([dfEval[action_col_name].values[i] for action_col_name in action_col_names])
            stateBuffer.append(np.concatenate((dfEval_actions, netOutput)))

    if plot:
        __plot_results(input_col_names, action_col_names, dfNet, dfEval, window_size, mean, std)


def __plot_results(input_col_names, action_col_names, dfNet, dfEval, window_size, mean, std):
    now_str = datetime.now().strftime("%d%m%Y-%H%M%S")
    fig, axs = plt.subplots(len(input_col_names)+1, 1, figsize=(10, 15))

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

    fig.savefig(f'plots/plot-{window_size}-{now_str}.png')
    plt.show()