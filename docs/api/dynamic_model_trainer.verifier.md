<!-- markdownlint-disable -->

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\verifier.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `dynamic_model_trainer.verifier`





---

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\verifier.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `evaluate_model`

```python
evaluate_model(
    data_frame,
    input_col_names,
    action_col_names,
    target_col_names,
    window_size,
    mean,
    std,
    plot=True
)
```

Measures model quality and displays plotted results on demand 



**Args:**
 
 - <b>`data_frame`</b>:  Data 
 - <b>`input_col_names`</b>:  Names of the inputs 
 - <b>`action_col_names`</b>:  Names of the action inputs 
 - <b>`target_col_names`</b>:  Names of the targets 
 - <b>`window_size`</b>:  Number of past time steps that are taken into account 
 - <b>`plot`</b>:  Specifies whether plotting is desired 



**Todo:**
 * fix plotting error: ValueError: x and y must have same first dimension, but have shapes (0,) and (64,) * plot actions for different action spaces 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
