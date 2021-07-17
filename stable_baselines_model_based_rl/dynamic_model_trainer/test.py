import os
import dynamic_model_trainer

sample = True
log = True
evaluate_model = True
plot_results = True
export_model = True

if sample:
    gym_environment_name = 'CartPole-v1'
    episode_count = 20
    max_steps = 100
    dynamic_model_trainer.sample_environment_and_train_dynamic_model(gym_environment_name, episode_count, max_steps,
                                                                     log=True, evaluate_model=True, plot_results=True,
                                                                     export_model=True)
else:
    sample_output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../sample_output/')
    data_file_name = f'{sample_output_path}cartpole-v1_2021-07-17-13-01-18_sampled_data.csv'
    config_file_name = f'{sample_output_path}cartpole-v1_2021-07-17-13-03-13_config.yaml'
    dynamic_model_trainer.build_and_train_dynamic_model(data_file_name, config_file_name,
                                                        log=True, evaluate_model=True, plot_results=True,
                                                        export_model=True)
