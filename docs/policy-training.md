# Policy Training (with Stable Baselines)

You can use the `train_stable_baselines_policy` function from the `sb_training` module to train/
learn a stable baselines policy against a gym environment. It works for both, regular gym envs,
as well as for the wrapped gym env of this library.  
It is basically just a simple wrapper/ utility function to create the proper policy/model based
on the given configuration.

For more details, check out the `sb_policy_creation_example.py` script from the
`example_usage` directory, the API documentation of the above mentionend function, as well as
the documentation of stable baselines itself.

To make use of all stable baselines features, you can always manually pass and use the
wrapped gym environment.
