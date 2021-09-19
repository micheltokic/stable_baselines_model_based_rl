# Dynamic Model Training/Creation

## Process
The `dynamic_model_trainer.training` module is used to create and train a dynamic model of a gym environment. The module contains a single method `build_and_train_dynamic_model` that triggers the following process:

**1. Prepare data**

Data processing, executed in `prepare_data.prepare_data` includes the following steps:

- Importing the csv file as `pandas.DataFrame`
- Adding noise
- Dividing the data set into training, validation and test data
- Grouping of samples into fixed-length time-dependent series required for recurrent neural network training
- Calculating standard deviation and mean required for normalization

**2. Build dynamic model**

`model_builder.build_dynamic_model` reads the tensorflow model from the configuration file. Normalization layers are added to the front and back of the model, as well as a penultimate output layer in the correct dimension for the given problem. 

**3. Train the dynamic model**

**4. Verification**

In a final step, the training process is reviewed. For this purpose, methods are available in the `verifier` that check the model against the test data and display it graphically.  

**5. Save the dynamic model**


## Example Usage

```python
config = Configuration('path_to_config')
training.build_and_train_dynamic_model('path_to_csv', config, 'path_to_output')
```
