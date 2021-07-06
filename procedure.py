# 1. train mit der env / daten
# 2. train liefert model 
# 3. create erstellt die env basierend auf das model 
# --- obere schritte können zusammengefasst werden
# 4. run/step

# SAMPLING
  # def sample_input_and_config(gym_environment_name)
  #   return config_file, data_file

  # def sample_input_file(gym_environment_name)
  #   return data_file

  # def sample_input(gym_environment_name)
  #   return data

  
# TRAINING
  # def __read_config_file(config_file_name)
  #     config_file = read(config_file_name)
  #     return input_dimension, output_dimension, data, gym_environment_name, reinforcement_learning_algorithm
  
  # def __build_model(input_dimension, output_dimension, model_topology)
  #     return pytorch_model
  
  # def __train_model(data, reinforcement_learning_algorithm)
  #     return trained_pytorch_model
  
  # def __export_model(trained_pytorch_model)
  #     return exported_model_file
  
  # def create_and_train_model(input, config_file_name)
  #     input_dimension, output_dimension, data, gym_environment_name, reinforcement_learning_algorithm = __read_config_file(config_file_name)
  #     pytorch_model = __build_model()
  #     data = data == null ? sample_input(gym_environment_name) : data
  #     trained_pytorch_model = __train_model(data, reinforcement_learning_algorithm)
  #     return trained_pytorch_model

  # def create_train_and_export_model(input, config_file_name)
  #     trained_pytorch_model = create_and_train_model(input, config_file_name)
  #     exported_model_file = __export_model(trained_pytorch_model)
  #     return exported_model_file

  
# CAPSULE (Rewards, done states ? => gym_config_file ?)
  # def create_gym_environment (exported_model_file, gym_config_file_name)
  #   return gym_environment (with overwritten step method)
  
  # def create_gym_environment (trained_pytorch_model, gym_config_file_name)
  #   return gym_environment (with overwritten step method)
  
  # def create_and_train_gym_environment(input, config_file_name, gym_config_file_name)
  #   trained_pytorch_model = create_and_train_model(input, config_file_name)
  #   gym_environment = create_gym_environment(trained_pytorch_model)
  #   return gym_environment
  

# RUN (extend gym_environement with run and step method ?)
  # def run(model, gym_environment_name)
  # return simulated_ui
  #
  #   Teil des Frameworks oder nur zum Testen ?
  # def train_against(model)
  # return train_against_model
  #   
  #   Wenn möglich Teil des Frameworks
  # def plot(daten)
  #     plot
