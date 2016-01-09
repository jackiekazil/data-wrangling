import ConfigParser

def get_config(env):
    config = ConfigParser.ConfigParser()
    if env == 'PROD':
        return config.read(['config/production.cfg'])
    elif env == 'TEST':
        return config.read(['config/test.cfg'])
    return config.read(['config/development.cfg'])


def api_login():
    config = get_config('PROD')
    my_client = get_client(config.get('api_login', 'user'),
                           config.get('api_login', 'auth_key'))
    return my_client
