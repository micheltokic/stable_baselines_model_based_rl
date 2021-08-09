from utils.noise import add_fake_noise, add_gaussian_noise
import tensorflow as tf
import numpy as np


def prepare_data(df, input_col, target_col, window_size, training_batch_size=10, validation_batch_size=10,
                 training_pattern_percent=0.7, noise_settings={}):
    """
    Reads the data of the data frame,
    Converts them into a dataset readable by tensorflow and splits trainings and validation data.
    Additionally, the standard deviation and the average of the data are determined.

    Args:
        df: DataFrame with sampled Data from a gym environment.
        input_col: List with the names of the input columns.
        target_col: List with the names of the target columns.
        window_size: Number of past time steps that are taken into account
        training_batch_size: Bach size used for training
        validation_batch_size: Bach size used for validation
        training_pattern_percent: Relationship between training and validation data
        noise_settings: noise settings

    Returns:
        train_data: Training data set
        val_data: Validation data set
        input_shape: Shape of the input
        mean_in: Mean of the inputs
        std_in: Standard deviation of the inputs
        mean_out: Mean of the targets
        std_out: Standard deviation of the targets
    """
    
    if noise_settings:
        print("Generate noise on the target vectors")
        df = add_gaussian_noise(df, target_col, **noise_settings)
    
    ((x_train_multi, y_train_multi), (x_val_multi, y_val_multi)), mean_in, std_in, mean_out, std_out = \
        __create_training_data(df, input_col, target_col, window_size=window_size,
                               training_pattern_percent=training_pattern_percent)

    print('trainData: Single window of past history : {}'.format(x_train_multi[0].shape))
    print('trainData: Single window of future : {}'.format(y_train_multi[1].shape))
    print('valData: Single window of past history : {}'.format(x_val_multi[0].shape))
    print('valData: Single window of future : {}'.format(y_val_multi[1].shape))
    print('trainData: number of trainingsexamples: {}'.format(x_train_multi.shape))
    print('valData: number of trainingsexamples: {}'.format(x_val_multi.shape))

    train_data = tf.data.Dataset.from_tensor_slices((x_train_multi, y_train_multi))
    # train_data = train_data.cache().shuffle(max_training_pattern).batch(training_batch_size).repeat()
    train_data = train_data.shuffle(x_train_multi.shape[0]).batch(training_batch_size).repeat()

    val_data = tf.data.Dataset.from_tensor_slices((x_val_multi, y_val_multi))
    val_data = val_data.batch(validation_batch_size).repeat()
    input_shape = x_train_multi[0].shape[-2:]
    return train_data, val_data, input_shape, mean_in, std_in, mean_out, std_out


def __create_training_data(data, input_col, target_col, window_size=1, training_pattern_percent=0.7):
    data_train = data

    mean_in, std_in = __mean_and_std(input_col, data_train)
    mean_out, std_out = __mean_and_std(target_col, data_train)
    # data_plot.plot_hist_df(data_train, input_col)
    # data_plot.plot_timeseries_df(data_train, input_col)
    print(f"mean in = {mean_in}")
    print(f"std in = {std_in}")
    print(f"mean out =  {mean_out}")
    print(f"std out = {std_out}")

    grouped = data_train.groupby(['EPISODE'])

    inputs_all = []
    labels_all = []

    for g in grouped:
        # be sure that data inside a group is not shuffled # not sure if needed
        g = g[1].sort_values(by='STEP')

        past_history = window_size  # t-3, t-2, t-1, t
        future_target = 0  # t+1
        STEP = 1  # no subsampling of rows in data, e.g. only every i'th row

        # use pandas.DataFrame.values in order to get an numpy array from an pandas.DataFrame object

        input, labels = __multivariate_data(dataset=g[input_col][:].values, target=g[target_col][:].values,
                                            start_index=0, end_index=g[input_col][:].values.shape[0] - future_target,
                                            history_size=past_history, target_size=future_target, step=STEP,
                                            single_step=True)

        ## Append data to whole set of patterns
        for i in range(0, len(input)):
            inputs_all.append(input[i])
            labels_all.append(labels[i])

    length = len(inputs_all)

    c = list(zip(inputs_all, labels_all))
    np.random.shuffle(c)
    inputs_all, labels_all = zip(*c)

    split = int(training_pattern_percent * length)

    inputs_all = np.array(inputs_all)
    labels_all = np.array(labels_all)

    return ((inputs_all[0:split], labels_all[0:split]),
            (inputs_all[split:], labels_all[split:])), mean_in, std_in, mean_out, std_out


def __mean_and_std(columns, data):
    mean = np.zeros(len(columns))
    std = np.zeros(len(columns))
    index = 0
    for c in columns:
        mean[index], std[index] = __get_normalizations(data[c])
        index = index + 1
    return mean, std


def __get_normalizations(data):
    mean = data.mean()
    std = data.std()
    return mean, std


def __multivariate_data(dataset, target, start_index, end_index, history_size,
                        target_size, step, single_step=False):
    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size

    for i in range(start_index, end_index):
        indices = range(i - history_size, i, step)
        data.append(dataset[indices])

        if single_step:
            labels.append(target[i + target_size])
        else:
            labels.append(target[i:i + target_size])

    return np.array(data), np.array(labels)
