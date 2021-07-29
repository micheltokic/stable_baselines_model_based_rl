<!-- markdownlint-disable -->

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\tensorflow_data_generator.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `dynamic_model_trainer.tensorflow_data_generator`





---

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\tensorflow_data_generator.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_data`

```python
prepare_data(
    df,
    input_col,
    target_col,
    window_size,
    training_batch_size=10,
    validation_batch_size=10,
    training_pattern_percent=0.7
)
```

Reads the data of the data frame, Converts them into a dataset readable by tensorflow and splits trainings and validation data. Additionally, the standard deviation and the average of the data are determined. 



**Args:**
 
 - <b>`df`</b>:  DataFrame with sampled Data from a gym environment. 
 - <b>`input_col`</b>:  List with the names of the input columns. 
 - <b>`target_col`</b>:  List with the names of the target columns. 
 - <b>`window_size`</b>:  Number of past time steps that are taken into account 
 - <b>`training_batch_size`</b>:  Bach size used for training 
 - <b>`validation_batch_size`</b>:  Bach size used for validation 
 - <b>`training_pattern_percent`</b>:  Relationship between training and validation data 



**Returns:**
 
 - <b>`train_data`</b>:  Training data set 
 - <b>`val_data`</b>:  Validation data set 
 - <b>`input_shape`</b>:  Shape of the input 
 - <b>`mean_in`</b>:  Mean of the inputs 
 - <b>`std_in`</b>:  Standard deviation of the inputs 
 - <b>`mean_out`</b>:  Mean of the targets 
 - <b>`std_out`</b>:  Standard deviation of the targets 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
