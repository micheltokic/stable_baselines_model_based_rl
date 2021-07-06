# 1. train mit der env / daten
# 2. train liefert model 
# 3. create erstellt die env basierend auf das model 
# --- obere schritte können zusammengefasst werden
# 4. run/step

# def train(input, config_file)
#     tensorflow/pytorch training on input data set
#     return exported_model_file
#
# def create_trained_model(gym_environment_name, steps, config_file)
#      env = gym.make(gym_environment_name)
#      return train(input, config_file)
#
#   Wie bei gym environments
# def step(model)
#
# 
# def run(model, gym_environment_name)
# return simulated_ui
#
#   Teil des Frameworks oder nur zum Testen ?
# def train_against(model)
# return train_against_model
#   
#   Teil des Frameworks oder nur zum Testen ?
# def plot(daten)
#     plot
