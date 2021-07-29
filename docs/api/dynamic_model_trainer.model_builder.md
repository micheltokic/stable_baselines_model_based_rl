<!-- markdownlint-disable -->

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\model_builder.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `dynamic_model_trainer.model_builder`





---

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\model_builder.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_dynamic_model`

```python
build_dynamic_model(model_config, optimizer, loss)
```

Creates and compiles a neural network consisting of a 'Long Short Term Memory' layer followed by a 'Dense' layer. 



**Args:**
 
 - <b>`input_shape`</b>:  Shape of the input 
 - <b>`model_config`</b>:  dictionary containing the model building configuration 
 - <b>`optimizer`</b>:  Optimizer used optimizing gradient descent 
 - <b>`loss`</b>:  loss function used calculating the error 



**Returns:**
 
 - <b>`dynamic_model`</b>:  Compiled tensorflow model with architecture given in the model_config dictionary 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
