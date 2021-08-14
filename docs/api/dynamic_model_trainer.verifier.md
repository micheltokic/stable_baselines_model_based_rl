<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\dynamic_model_trainer\verifier.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `dynamic_model_trainer.verifier`





---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\dynamic_model_trainer\verifier.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `evaluate_model`

```python
evaluate_model(
    data_frame,
    input_col_names,
    action_col_names,
    target_col_names,
    lag
)
```

Measures model quality and displays plotted results on demand 



**Args:**
 
 - <b>`data_frame`</b>:  Data 
 - <b>`input_col_names`</b>:  Names of the inputs 
 - <b>`action_col_names`</b>:  Names of the action inputs 
 - <b>`target_col_names`</b>:  Names of the targets 
 - <b>`lag`</b>:  Number of past time steps that are taken into account 



**Todo:**
 * fix plotting error: ValueError: x and y must have same first dimension, but have shapes (0,) and (64,) * plot actions for different action spaces 


---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\dynamic_model_trainer\verifier.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `plot_results`

```python
plot_results(
    input_col_names,
    action_col_names,
    dfNet,
    dfEval,
    window_size,
    mean,
    std
)
```






---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\dynamic_model_trainer\verifier.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `save`

```python
save(final_dir_path, model, loss, lag, fig, config, data_path)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
