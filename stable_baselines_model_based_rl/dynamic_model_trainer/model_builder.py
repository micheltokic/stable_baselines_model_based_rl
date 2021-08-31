import yaml
import keras
from keras.layers import Dense, Normalization
from keras.models import Sequential, Model
import tensorflow as tf


def build_dynamic_model(model_config, input_shape, mean_in, std_in, mean_out, std_out, output_len, optimizer, loss):
    """
    Creates and compiles a neural network consisting of a 'Long Short Term Memory' layer followed by a 'Dense' layer.

    Args:
        model_config: dictionary containing the model building configuration
        output_len: Length of the output vector
        optimizer: Optimizer used optimizing gradient descent
        loss: loss function used calculating the error

    Returns:
        dynamic_model: Compiled tensorflow model with architecture given in the model_config dictionary
    """

    yaml_model_config = yaml.dump(model_config)
    dynamic_model = keras.models.model_from_yaml(yaml_model_config, custom_objects=None)
    layers = dynamic_model.layers

    dynamic_model = Sequential()
    dynamic_model.add(tf.keras.layers.Lambda(lambda x: (x - mean_in) / std_in, input_shape=input_shape))

    for layer in layers:
        dynamic_model.add(layer)

    dynamic_model.add(Dense(output_len))

    def loss(y_true, y_pred):
        y_true_n = tf.divide(tf.subtract(y_true, mean_out), std_out)
        y_pred_n = tf.divide(tf.subtract(y_pred, mean_out), std_out)
        return tf.keras.losses.MSE(y_true_n, y_pred_n)

    dynamic_model.compile(optimizer=optimizer, loss=loss)

    return dynamic_model
