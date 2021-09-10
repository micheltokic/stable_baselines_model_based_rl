import yaml
import keras
from keras.layers import Dense, Lambda
from keras.models import Sequential
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
    dynamic_model: Sequential = keras.models.model_from_yaml(yaml_model_config, custom_objects=None)

    # normalization layer (first layer)
    dynamic_model.layers.insert(0, Lambda(lambda x, mean, std: (x - mean) / std,
                                          input_shape=input_shape,
                                          arguments={'mean': mean_in, 'std': std_in}))
    # layer for correct output shape
    dynamic_model.add(Dense(output_len))
    # revert normalization layer (last layer)
    dynamic_model.add(Lambda(lambda x, mean, std: (x * std) + mean,
                             arguments={'mean': mean_out, 'std': std_out}))

    def loss(y_true, y_pred):
        y_true_n = tf.divide(tf.subtract(y_true, mean_out), std_out)
        y_pred_n = tf.divide(tf.subtract(y_pred, mean_out), std_out)
        return tf.keras.losses.MSE(y_true_n, y_pred_n)

    dynamic_model.compile(optimizer=optimizer, loss=loss)

    return dynamic_model
