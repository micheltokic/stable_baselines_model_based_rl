from stable_baselines_model_based_rl.utils.configuration import Configuration


def test_configuration_set_and_get(mocker):
    mocker.patch(
        'stable_baselines_model_based_rl.utils.configuration.Configuration.load_config_from_file')
    config = Configuration('foo')
    config.config = {}

    assert config.config == {}

    config.set('foo.bar', 'test')
    expected_config = {'foo': {'bar': 'test'}}
    assert config.config == expected_config

    config.set('nested.list', [1, 2, 3])
    expected_config['nested'] = {'list': [1, 2, 3]}
    assert config.config == expected_config

    config.set('nested.list', 'nowastring')
    expected_config['nested']['list'] = 'nowastring'
    assert config.config == expected_config

    config.set('key', 12)
    config.set('key2', {'foo': 'bar'})
    config.set('key3', (1, 2, 3, 'string'))
    expected_config['key'] = 12
    expected_config['key2'] = {'foo': 'bar'}
    expected_config['key3'] = (1, 2, 3, 'string')
    assert config.config == expected_config



def test_configuration_get_default(mocker):
    mocker.patch(
        'stable_baselines_model_based_rl.utils.configuration.Configuration.load_config_from_file')
    config = Configuration('foo')
    config.config = {}

    assert config.get('foo.bar') == None
    assert config.get('foo.bar', default='default') == 'default'
    assert config.get('foo.bar') == None

    config.set('new.key', [1,2,3])
    assert config.get('new.key', default='string') == [1,2,3]
