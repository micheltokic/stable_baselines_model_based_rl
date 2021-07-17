import tensorflow as tf
import numpy as np


def build_lstm(input_shape, mean_out, optimizer=tf.keras.optimizers.RMSprop(), lstm_len=50, loss="mse"):
    """
    Creates and compiles a neural network consisting of a 'Long Short Term Memory' layer followed by a 'Dense' layer.

    Args:
        input_shape: Shape of the input
        mean_out: Mean of the targets to determine dense layer length
        optimizer: Optimizer used by neural network for gradients calculations
        lstm_len: Length of the 'Long Short Term Memory' layer
        loss: Name of the loss function used for the error calculation by the neural network

    Returns:
        lstm_model: Compiled tensorflow model with one 'Long Short Term Memory' layer and one consecutive 'Dense' layer
    """

    lstm_model = tf.keras.models.Sequential()
    lstm_model.add(tf.keras.layers.LSTM(lstm_len, input_shape=input_shape, dtype=np.float64))
    lstm_model.add(tf.keras.layers.Dense(len(mean_out)))
    lstm_model.compile(optimizer=optimizer, loss=loss)

    return lstm_model
