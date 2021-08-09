import yaml
import keras
from keras.layers import Dense
from keras.models import Sequential


def build_dynamic_model(model_config, output_len, optimizer, loss):
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

    dynamic_model.add(Dense(output_len))

    dynamic_model.compile(optimizer=optimizer, loss=loss)

    return dynamic_model
